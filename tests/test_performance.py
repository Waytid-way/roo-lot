# tests/test_performance.py
import pytest
import time
from utils.model_predictor import ElectricityPredictor
from conversation.manager import ConversationManager

class TestPerformance:
    """Test performance and resource usage"""
    
    def test_prediction_speed(self, mocker):
        """Test: Prediction completes within acceptable time"""
        # Mock actual model loading to focus on code overhead not disk I/O
        mocker.patch('joblib.load') 
        mocker.patch('os.path.exists', return_value=True)
        
        predictor = ElectricityPredictor()
        
        # Inject mock model
        mock_model = mocker.Mock()
        mock_model.predict.return_value = [1000]
        predictor.model = mock_model
        
        mock_scaler = mocker.Mock()
        mock_scaler.transform.return_value = [[0,0,0,0,0]]
        predictor.scaler = mock_scaler
        
        test_input = {
            'ac_hours': 8,
            'room_size': 30,
            'fan_hours': 10,
            'num_appliances': 5,
            'occupants': 2
        }
        
        start_time = time.time()
        for _ in range(100):
            result = predictor.predict(test_input)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 100
        
        assert avg_time < 0.05  # Should be very fast (< 50ms) without I/O
        assert result is not None
    
    def test_manager_initialization_speed(self, mocker):
        """Test: Manager creation is fast"""
        class SessionState(dict):
            def __getattr__(self, key):
                if key in self: return self[key]
                raise AttributeError(f"SessionState has no attribute '{key}'")
            def __setattr__(self, key, value):
                self[key] = value
                
        mock_state = SessionState()
        mocker.patch('streamlit.session_state', mock_state)
        
        start_time = time.time()
        for _ in range(100):
             ConversationManager()
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 100
        assert avg_time < 0.01  # Should be instant
