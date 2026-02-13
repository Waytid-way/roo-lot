
"""
Roo-Lot Chatbot - Model Predictor (Updated for Kaggle Dataset)
"""
import pandas as pd
import joblib
import os
import streamlit as st
import datetime
import time
from typing import Union, Dict, Any, List

class ElectricityPredictor:
    def __init__(self):
        self.model = self._load_model()
        # Scale is part of the electricbills_predict.pkl pipeline now!
        # But we keep scaler.pkl loading as fallback or for manual inspection if needed.
        self.scaler = None 

    def _load_model(self):
        try:
            base_path = os.path.dirname(os.path.dirname(__file__))
            models_path = os.path.join(base_path, 'models')
            
            # Load best model (pipeline)
            if os.path.exists(os.path.join(models_path, 'electricbills_predict.pkl')):
                return joblib.load(os.path.join(models_path, 'electricbills_predict.pkl'))
            
            # Fallback
            if os.path.exists(os.path.join(models_path, 'model_optimized.pkl')):
                st.warning("Using old model fallback!")
                return joblib.load(os.path.join(models_path, 'model_optimized.pkl'))
                
            return None
        except Exception as e:
            st.error(f"Error loading model: {e}")
            return None

    def predict(self, inputs: dict) -> dict:
        """
        Generate prediction from user inputs
        
        Args:
            inputs (dict): Dictionary with keys 'household_size', 'has_ac', 'month'
            
        Returns:
            dict: Prediction results including 'amount', 'kwh', 'range', 'breakdown'
        
        Features expected by model: ['household_size', 'has_ac', 'season_hot', 'season_rainy', 'weekend_ratio']
        """
        if not self.model:
            return None

        try:
            # 1. Parse Inputs with Validation
            household_size = int(inputs.get('household_size', 1))
            
            # Validate household size
            if not 1 <= household_size <= 10:
                st.error("⚠️ จำนวนสมาชิกต้องอยู่ระหว่าง 1-10 คน")
                return None
            
            # Extrapolation warning
            if household_size > 6:
                st.warning(
                    f"⚠️ Model เทรนด้วยข้อมูลบ้านไม่เกิน 6 คน "
                    f"(คุณกรอก {household_size} คน) ค่าทำนายอาจคลาดเคลื่อนสูง"
                )
            
            # Parse has_ac - Handle both old format (ac_hours) and new format (choice)
            has_ac_input = inputs.get('has_ac', 0)
            
            if isinstance(has_ac_input, str):
                # New format: "มี" or "ไม่มี"
                has_ac = 1 if has_ac_input == "มี" else 0
            elif isinstance(has_ac_input, (int, float)):
                # Old format compatibility or direct 0/1
                has_ac = 1 if float(has_ac_input) > 0 else 0
            else:
                has_ac = 0

            # Month parsing
            month_input = inputs.get('month', 1)
            month = self._parse_month(month_input)
            
            if not 1 <= month <= 12:
                st.error("⚠️ เดือนไม่ถูกต้อง")
                return None
            
            # 2. Derive Features (Logic from data_pipeline.py)
            season = self._get_season(month)
            season_hot = 1 if season == 'hot' else 0
            season_rainy = 1 if season == 'rainy' else 0
            
            # Weekend Ratio (Use 2025 as reference year for consistency with training data)
            weekend_ratio = self._calculate_weekend_ratio(2025, month)
            
            # 3. Create DataFrame
            input_data = pd.DataFrame([{
                'household_size': household_size,
                'has_ac': has_ac,
                'season_hot': season_hot,
                'season_rainy': season_rainy,
                'weekend_ratio': weekend_ratio
            }])
            
            # 4. Predict (Model is a Pipeline, handles scaling)
            start_time = time.time()
            predicted_kwh = self.model.predict(input_data)[0]
            elapsed_time = time.time() - start_time
            print(f"⏱️ Prediction time: {elapsed_time:.4f}s")
            
            # IMPORTANT: Model outputs MONTHLY kWh already (not daily)!
            # Training data used monthly consumption values (100-800 kWh/month range)
            monthly_kwh = predicted_kwh  # NO *30 multiplication!
            
            # 5. Convert to Baht (Approx 4.2 THB/unit + FT)
            prediction_baht = monthly_kwh * 4.2
            
            # 6. Result Structure - NO FABRICATED BREAKDOWN!
            # Report says model outputs total only, not AC vs Appliances
            return {
                'amount': round(prediction_baht, 2),
                'kwh': round(monthly_kwh, 2),
                'range': round(14.58 * 4.2, 2),  # MAE from generate_correct_plots.py: 14.58 kWh (monthly basis)
                'details': input_data.to_dict(orient='records')[0],
                # Removed fabricated breakdown - model doesn't output this!
                'model_metrics': {
                    'r2_score': 0.9888,  # From generate_correct_plots.py
                    'mae': 14.58,         # MAE in kWh (monthly)
                    'rmse': 18.56         # RMSE in kWh (monthly)
                }
            }
        except Exception as e:
            st.error(f"Prediction error: {str(e)}")
            return None

    def _parse_month(self, month_input):
        # Dictionary for Thai months if needed
        thai_months = {
            "มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4, "พฤษภาคม": 5, "มิถุนายน": 6,
            "กรกฎาคม": 7, "สิงหาคม": 8, "กันยายน": 9, "ตุลาคม": 10, "พฤศจิกายน": 11, "ธันวาคม": 12
        }
        if isinstance(month_input, int):
            return month_input
        if isinstance(month_input, str):
            if month_input.isdigit():
                return int(month_input)
            for name, val in thai_months.items():
                if name in month_input:
                    return val
        return 1 # Default Jan

    def _get_season(self, month):
        # Match training script logic!
        if month in [3, 4, 5, 6]:
            return 'hot'
        elif month in [7, 8, 9, 10]:
            return 'rainy'
        else:
            return 'cool'

    def _calculate_weekend_ratio(self, year, month):
        # Match training logic exactly
        try:
            days_in_month = pd.Period(f"{year}-{month}").days_in_month
            dates = pd.date_range(f"{year}-{month}-01", f"{year}-{month}-{days_in_month}")
            weekend_count = dates.dayofweek.isin([5, 6]).sum()
            return weekend_count / days_in_month
        except:
            return 0.28 # Fallback average from training data
