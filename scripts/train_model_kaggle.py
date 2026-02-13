"""
Roo-Lot: Model Training Pipeline for Kaggle-aligned Dataset
Features: household_size, has_ac, season_hot, season_rainy, weekend_ratio
Target: energy_consumption_kwh (monthly basis)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
import joblib
import os
from datetime import datetime

def create_seasonal_features(df):
    """Add season features matching model_predictor.py logic"""
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    
    # Season features (match _get_season() in model_predictor.py)
    # hot: Mar-Jun (3,4,5,6), rainy: Jul-Oct (7,8,9,10), cool: Nov-Feb (11,12,1,2)
    df['season_hot'] = df['month'].isin([3, 4, 5, 6]).astype(int)
    df['season_rainy'] = df['month'].isin([7, 8, 9, 10]).astype(int)
    
    # Weekend ratio calculation
    def calc_weekend_ratio(date):
        year, month = date.year, date.month
        days_in_month = pd.Period(f"{year}-{month}").days_in_month
        month_dates = pd.date_range(f"{year}-{month}-01", periods=days_in_month, freq='D')
        weekend_days = month_dates.dayofweek.isin([5, 6]).sum()
        return weekend_days / days_in_month
    
    df['weekend_ratio'] = df['date'].apply(calc_weekend_ratio)
    
    return df

def generate_synthetic_data(n_samples=1000):
    """Generate synthetic data matching the report's domain"""
    print("📊 Generating synthetic training data (Kaggle-aligned)...")
    
    np.random.seed(42)
    
    data = {
        'household_size': np.random.randint(1, 11, n_samples),  # 1-10 people
        'has_ac': np.random.randint(0, 2, n_samples),  # 0 or 1
        'avg_temperature': np.random.normal(30, 5, n_samples)
    }
    df = pd.DataFrame(data)
    
    # Generate dates across 2025
    dates = pd.date_range(start='2025-01-01', end='2025-12-31')
    df['date'] = np.random.choice(dates, n_samples)
    
    # Feature Engineering
    df = create_seasonal_features(df)
    
    # Target Generation (MONTHLY kWh)
    # Formula: Base + 50*Size + 200*AC + SeasonEffect + Noise
    df['energy_consumption_kwh'] = (
        100 +  # Base consumption
        50 * df['household_size'] +  # Per person
        200 * df['has_ac'] +  # AC impact
        20 * df['season_hot'] -  # Hot season increase
        10 * df['season_rainy'] +  # Rainy season decrease
        np.random.normal(0, 20, n_samples)  # Noise
    )
    
    # Ensure positive values
    df['energy_consumption_kwh'] = df['energy_consumption_kwh'].clip(lower=50)
    
    return df

def train_model():
    print("=" * 70)
    print("ROO-LOT: MODEL TRAINING (KAGGLE-ALIGNED FEATURES)")
    print("=" * 70)
    
    # Try to load existing data, otherwise generate synthetic
    data_path = 'data/household_energy.csv'
    if os.path.exists(data_path):
        print(f"\n✅ Loading data from {data_path}")
        df = pd.read_csv(data_path)
        
        # Ensure features exist
        if 'date' not in df.columns or 'season_hot' not in df.columns:
            print("⚠️ Missing derived features, regenerating...")
            df = create_seasonal_features(df)
    else:
        print(f"\n⚠️ {data_path} not found, generating synthetic data...")
        df = generate_synthetic_data(n_samples=1000)
    
    print(f"📊 Loaded {len(df):,} samples")
    
    # Select features (MUST match model_predictor.py)
    feature_cols = ['household_size', 'has_ac', 'season_hot', 'season_rainy', 'weekend_ratio']
    target_col = 'energy_consumption_kwh'
    
    X = df[feature_cols]
    y = df[target_col]
    
    print(f"\n📋 Features: {feature_cols}")
    print(f"🎯 Target: {target_col}")
    print(f"\n📈 Target Statistics (Monthly kWh):")
    print(f"   Min:    {y.min():.2f} kWh")
    print(f"   Max:    {y.max():.2f} kWh")
    print(f"   Mean:   {y.mean():.2f} kWh")
    print(f"   Median: {y.median():.2f} kWh")
    
    # Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"\n🔀 Split: {len(X_train):,} train / {len(X_test):,} test")
    
    # Build Pipeline (Scaling + Model)
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', RandomForestRegressor(random_state=42, n_jobs=-1))
    ])
    
    # Hyperparameter tuning
    param_grid = {
        'model__n_estimators': [100, 200],
        'model__max_depth': [10, 15, None],
        'model__min_samples_split': [2, 5]
    }
    
    print("\n🔍 Running GridSearchCV (5-fold CV)...")
    grid_search = GridSearchCV(
        pipeline, param_grid, cv=5, scoring='r2', n_jobs=-1, verbose=1
    )
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    print(f"\n✅ Best Params: {grid_search.best_params_}")
    
    # Evaluate
    y_train_pred = best_model.predict(X_train)
    y_test_pred = best_model.predict(X_test)
    
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    
    print("\n" + "=" * 70)
    print("📊 MODEL PERFORMANCE")
    print("=" * 70)
    print(f"Train R²:  {train_r2:.4f}")
    print(f"Test R²:   {test_r2:.4f}")
    print(f"Test MAE:  {test_mae:.2f} kWh")
    print(f"Test RMSE: {test_rmse:.2f} kWh")
    
    # Feature Importance
    rf_model = best_model.named_steps['model']
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n🔬 Feature Importance:")
    print(feature_importance.to_string(index=False))
    
    # Save model
    os.makedirs('models', exist_ok=True)
    model_path = 'models/electricbills_predict.pkl'
    joblib.dump(best_model, model_path)
    
    print(f"\n💾 Model saved: {model_path}")
    
    # Sanity check
    print("\n" + "=" * 70)
    print("🧪 SANITY CHECK (Expected: 100-800 kWh, 400-3500 THB)")
    print("=" * 70)
    
    test_cases = [
        {'household_size': 1, 'has_ac': 0, 'season_hot': 0, 'season_rainy': 0, 'weekend_ratio': 0.25},
        {'household_size': 2, 'has_ac': 1, 'season_hot': 1, 'season_rainy': 0, 'weekend_ratio': 0.29},
        {'household_size': 5, 'has_ac': 1, 'season_hot': 1, 'season_rainy': 0, 'weekend_ratio': 0.26},
        {'household_size': 6, 'has_ac': 0, 'season_hot': 0, 'season_rainy': 1, 'weekend_ratio': 0.32}
    ]
    
    all_valid = True
    for i, case in enumerate(test_cases, 1):
        pred_kwh = best_model.predict(pd.DataFrame([case]))[0]
        pred_thb = pred_kwh * 4.2
        
        print(f"\nCase {i}:")
        print(f"  Input: {case}")
        print(f"  Output: {pred_kwh:.2f} kWh ({pred_thb:.2f} THB)")
        
        # Validate range (monthly should be 50-1000 kWh)
        if pred_kwh < 50 or pred_kwh > 1000:
            print(f"  ⚠️ WARNING: Prediction outside reasonable range!")
            all_valid = False
        else:
            print(f"  ✅ Valid range")
    
    print("\n" + "=" * 70)
    if all_valid:
        print("✅ ALL SANITY CHECKS PASSED!")
    else:
        print("⚠️ SOME CHECKS FAILED - Review model logic")
    print("=" * 70)
    
    return best_model

if __name__ == "__main__":
    train_model()
