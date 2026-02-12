# tests/test_model_predictor.py
import pytest
import pandas as pd
import numpy as np
from utils.model_predictor import ElectricityPredictor
from pathlib import Path
import os
import joblib

class TestElectricityPredictor:
    """Test ML model prediction logic"""
    
    @pytest.fixture
    def predictor(self):
        # We might need to mock _load_model and _load_scaler if files don't exist
        # But for now let's try to instantiate it and see if it handles missing files gracefully 
        # or if we should mock it for the test to pass even without models.
        # The code catches exceptions and returns None/prints error.
        return ElectricityPredictor()
    
    def test_model_loading(self, predictor):
        """Test: Model loads or handles missing model gracefully"""
        # If model exists, it should be loaded. If not, predictor.model might be None.
        # This test just ensures __init__ doesn't crash.
        assert hasattr(predictor, 'model')
        assert hasattr(predictor, 'scaler')
    
    def test_valid_prediction(self, predictor, mocker):
        """Test: Valid inputs produce reasonable predictions"""
        # Mock model and scaler to ensure test passes regardless of actual model files
        mock_model = mocker.Mock()
        mock_model.predict.return_value = np.array([1500.0])
        predictor.model = mock_model
        
        mock_scaler = mocker.Mock()
        mock_scaler.transform.return_value = np.array([[0.5, 0.5, 0.5, 0.5, 0.5]])
        predictor.scaler = mock_scaler
        
        valid_input = {
            'ac_hours': 8,
            'room_size': 30,
            'fans': 2,
            'lights': 2,
            'computers': 1,
            'other_appliances': 0
        }
        
        result = predictor.predict(valid_input)
        
        assert result is not None
        assert 'amount' in result
        assert result['amount'] == 1500.0
        assert 'breakdown' in result

    def test_prediction_calculation(self, predictor, mocker):
        """Test: Breakdown calculations are correct based on prediction"""
        mock_model = mocker.Mock()
        mock_model.predict.return_value = np.array([1000.0])
        predictor.model = mock_model
        
        mock_scaler = mocker.Mock()
        mock_scaler.transform.return_value = np.array([[0.1]])
        predictor.scaler = mock_scaler
        
        inputs = {'ac_hours': 0, 'room_size': 0} # Dummy inputs
        result = predictor.predict(inputs)
        
        assert result['amount'] == 1000.0
        assert result['breakdown']['ac_cost'] == 600.0  # 60%
        assert result['breakdown']['appliances_cost'] == 300.0 # 30%
        assert result['breakdown']['base_fee'] == 100.0 # 10%
    
    def test_missing_model_handling(self, predictor):
        """Test: Returns None if model/scaler is missing"""
        predictor.model = None
        result = predictor.predict({})
        assert result is None

    def test_input_preprocessing(self, predictor, mocker):
        """Test: Inputs are correctly transformed into DataFrame columns"""
        mock_scaler = mocker.Mock()
        mock_scaler.transform.return_value = np.array([[0]]) # Return dummy
        predictor.scaler = mock_scaler
        predictor.model = mocker.Mock()
        predictor.model.predict.return_value = [0]
        
        inputs = {
            'ac_hours': 5,
            'room_size': 25,
            'fans': 2,
            'lights': 3,
            'computers': 0,
            'other_appliances': 1
        }
        
        # We need to spy on scaler.transform to see what was passed
        predictor.predict(inputs)
        
        # Check arguments passed to transform
        args, _ = mock_scaler.transform.call_args
        df = args[0]
        
        assert isinstance(df, pd.DataFrame)
        assert df.iloc[0]['ac_hours_per_day'] == 5
        assert df.iloc[0]['room_area'] == 25
        assert df.iloc[0]['num_appliances'] == 6 # 2+3+0+1
