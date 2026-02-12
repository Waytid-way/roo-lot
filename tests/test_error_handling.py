# tests/test_error_handling.py
import pytest
from pathlib import Path
import shutil
import streamlit as st

class TestErrorHandling:
    """Test error scenarios and recovery"""
    
    def test_missing_model_file(self, mocker):
        """Test: Graceful handling when model file is missing"""
        # We can mock os.path.exists to return False
        mocker.patch('os.path.exists', return_value=False)
        mocker.patch('streamlit.error') # Suppress error output
        
        from utils.model_predictor import ElectricityPredictor
        predictor = ElectricityPredictor()
        
        # Should handle missing file gracefully (model is None)
        assert predictor.model is None
    
    def test_corrupted_session_state(self, mocker):
        """Test: Recovery from corrupted session state"""
        class SessionState(dict):
            def __getattr__(self, key):
                if key in self: return self[key]
                raise AttributeError(f"SessionState has no attribute '{key}'")
            def __setattr__(self, key, value):
                self[key] = value

        # Mock st.session_state with missing keys
        mock_state = SessionState()
        mocker.patch('streamlit.session_state', mock_state)
        
        from conversation.manager import ConversationManager
        
        # When initializing manager, it should repair the state
        # The __init__ calls _initialize_session_state which checks keys
        manager = ConversationManager()
        
        # Verify keys are restored
        assert 'conversation_stage' in mock_state
        assert 'messages' in mock_state
    
    def test_invalid_prediction_input(self, mocker):
        """Test: Predictor handles bad input types"""
        from utils.model_predictor import ElectricityPredictor
        
        # Mock successful model load so we can test predict method
        # If we just instantiate, it might fail to load model, that's fine, 
        # but we need to inject a mock model to test predict's error handling for inputs
        
        predictor = ElectricityPredictor()
        mock_model = mocker.Mock()
        mock_model.predict.side_effect = Exception("Model error")
        predictor.model = mock_model
        predictor.scaler = mocker.Mock()
        
        # Should catch exception and return None/Error
        mocker.patch('streamlit.error')
        result = predictor.predict({'ac_hours': 'NaN'})
        
        assert result is None
