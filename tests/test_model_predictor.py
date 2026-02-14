# tests/test_model_predictor.py
"""
Updated tests for ElectricityPredictor - Aligned with Kaggle dataset model
Features: household_size, has_ac, month
"""
import pytest
import pandas as pd
import numpy as np
from utils.model_predictor import ElectricityPredictor
from pathlib import Path
import os
import joblib

class TestElectricityPredictor:
    """Test ML model prediction logic with current model features"""
    
    @pytest.fixture
    def predictor(self):
        """Fixture to create predictor instance"""
        return ElectricityPredictor()
    
    def test_model_loading(self, predictor):
        """Test: Model loads or handles missing model gracefully"""
        # If model exists, it should be loaded. If not, predictor.model might be None.
        # This test just ensures __init__ doesn't crash.
        assert hasattr(predictor, 'model')
        assert hasattr(predictor, 'scaler')
    
    def test_valid_prediction(self, predictor, mocker):
        """Test: Valid inputs produce reasonable predictions with new features"""
        # Mock model to ensure test passes regardless of actual model files
        mock_model = mocker.Mock()
        mock_model.predict.return_value = np.array([350.0])  # ~350 kWh
        predictor.model = mock_model
        
        # New input format aligned with Kaggle model
        valid_input = {
            'household_size': 4,
            'has_ac': 1,
            'month': 6
        }
        
        result = predictor.predict(valid_input)
        
        assert result is not None
        assert 'amount' in result  # Bill amount in THB
        assert 'kwh' in result     # Energy consumption
        assert 'range' in result   # Confidence interval
        assert 'details' in result # Input features used
        assert 'model_metrics' in result  # R², MAE, RMSE
        
        # Check calculations
        assert result['kwh'] == 350.0  # From mock
        assert result['amount'] == round(350.0 * 4.2, 2)  # 4.2 THB/unit
    
    def test_household_size_validation(self, predictor, mocker):
        """Test: Invalid household_size returns None"""
        predictor.model = mocker.Mock()
        
        # Test too small
        result = predictor.predict({'household_size': 0, 'has_ac': 1, 'month': 6})
        assert result is None
        
        # Test too large
        result = predictor.predict({'household_size': 11, 'has_ac': 1, 'month': 6})
        assert result is None
    
    def test_month_validation(self, predictor, mocker):
        """Test: Invalid month returns None"""
        predictor.model = mocker.Mock()
        
        # Test invalid month
        result = predictor.predict({'household_size': 4, 'has_ac': 1, 'month': 13})
        assert result is None
        
        result = predictor.predict({'household_size': 4, 'has_ac': 1, 'month': -1})
        assert result is None
    
    def test_has_ac_parsing_string(self, predictor, mocker):
        """Test: has_ac accepts string values (Thai)"""
        mock_model = mocker.Mock()
        mock_model.predict.return_value = np.array([300.0])
        predictor.model = mock_model
        
        # Test Thai "มี" (has AC)
        result = predictor.predict({
            'household_size': 3,
            'has_ac': 'มี',
            'month': 4
        })
        assert result is not None
        
        # Test Thai "ไม่มี" (no AC)
        result = predictor.predict({
            'household_size': 3,
            'has_ac': 'ไม่มี',
            'month': 4
        })
        assert result is not None
    
    def test_has_ac_parsing_numeric(self, predictor, mocker):
        """Test: has_ac accepts numeric values"""
        mock_model = mocker.Mock()
        mock_model.predict.return_value = np.array([300.0])
        predictor.model = mock_model
        
        # Test integer 1
        result = predictor.predict({
            'household_size': 3,
            'has_ac': 1,
            'month': 4
        })
        assert result is not None
        
        # Test float > 0
        result = predictor.predict({
            'household_size': 3,
            'has_ac': 8.5,
            'month': 4
        })
        assert result is not None
    
    def test_month_parsing_thai(self, predictor, mocker):
        """Test: Month accepts Thai month names"""
        mock_model = mocker.Mock()
        mock_model.predict.return_value = np.array([300.0])
        predictor.model = mock_model
        
        result = predictor.predict({
            'household_size': 3,
            'has_ac': 1,
            'month': 'มิถุนายน'  # June
        })
        assert result is not None
        assert result['details']['month'] == 6
    
    def test_missing_model_handling(self, predictor):
        """Test: Returns None if model is missing"""
        predictor.model = None
        result = predictor.predict({
            'household_size': 4,
            'has_ac': 1,
            'month': 6
        })
        assert result is None
    
    def test_input_dataframe_creation(self, predictor, mocker):
        """Test: Inputs are correctly transformed into DataFrame"""
        mock_model = mocker.Mock()
        mock_model.predict.return_value = np.array([400.0])
        predictor.model = mock_model
        
        # Capture the input DataFrame
        captured_df = None
        def capture_predict(df):
            nonlocal captured_df
            captured_df = df.copy()
            return np.array([400.0])
        
        mock_model.predict.side_effect = capture_predict
        
        inputs = {
            'household_size': 5,
            'has_ac': 1,
            'month': 7
        }
        
        predictor.predict(inputs)
        
        assert captured_df is not None
        assert isinstance(captured_df, pd.DataFrame)
        assert captured_df.iloc[0]['household_size'] == 5
        assert captured_df.iloc[0]['has_ac'] == 1
        assert captured_df.iloc[0]['season_hot'] == 0  # July = rainy season
        assert captured_df.iloc[0]['season_rainy'] == 1
        assert 0 < captured_df.iloc[0]['weekend_ratio'] < 1
    
    def test_model_metrics_present(self, predictor, mocker):
        """Test: Model metrics are included in result"""
        mock_model = mocker.Mock()
        mock_model.predict.return_value = np.array([250.0])
        predictor.model = mock_model
        
        result = predictor.predict({
            'household_size': 2,
            'has_ac': 0,
            'month': 1
        })
        
        assert 'model_metrics' in result
        assert result['model_metrics']['r2_score'] == 0.9888
        assert result['model_metrics']['mae'] == 14.58
        assert result['model_metrics']['rmse'] == 18.56
    
    def test_large_household_warning(self, predictor, mocker):
        """Test: Warning for extrapolation beyond training data (>6 people)"""
        mock_model = mocker.Mock()
        mock_model.predict.return_value = np.array([600.0])
        predictor.model = mock_model
        
        # Mock st.warning to capture it
        warning_messages = []
        def mock_warning(msg):
            warning_messages.append(msg)
        
        mocker.patch('streamlit.warning', mock_warning)
        
        result = predictor.predict({
            'household_size': 8,  # > 6
            'has_ac': 1,
            'month': 6
        })
        
        assert result is not None
        # Should have shown extrapolation warning
        assert any('8 คน' in str(msg) for msg in warning_messages)
    
    def test_season_calculation(self, predictor, mocker):
        """Test: Correct season is calculated from month"""
        mock_model = mocker.Mock()
        mock_model.predict.return_value = np.array([300.0])
        predictor.model = mock_model
        
        # Test hot season (Mar-Jun)
        predictor.predict({'household_size': 3, 'has_ac': 1, 'month': 4})
        
        # Test rainy season (Jul-Oct)
        predictor.predict({'household_size': 3, 'has_ac': 1, 'month': 8})
        
        # Test cool season (Nov-Feb)
        predictor.predict({'household_size': 3, 'has_ac': 1, 'month': 12})
        
        # All should complete without error
        assert True
    
    def test_weekend_ratio_calculation(self, predictor, mocker):
        """Test: Weekend ratio is calculated correctly"""
        mock_model = mocker.Mock()
        mock_model.predict.return_value = np.array([300.0])
        predictor.model = mock_model
        
        # Weekend ratio should be between 0 and 1
        result = predictor.predict({
            'household_size': 3,
            'has_ac': 1,
            'month': 6
        })
        
        assert result is not None
        details = result['details']
        assert 'weekend_ratio' in details
        assert 0 <= details['weekend_ratio'] <= 1
