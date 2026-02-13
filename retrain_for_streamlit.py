"""
Retrain model with Python 3.11 compatibility
This ensures the model works on Streamlit Cloud
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import json
from datetime import datetime
import sys

print(f"Python version: {sys.version}")
print("=" * 60)

# Load data
print("Loading data...")
df = pd.read_csv('data/household_energy.csv')

# Features for model
feature_cols = ['ac_hours_per_day', 'num_appliances', 'room_area', 'ac_temperature', 'num_people']
X = df[feature_cols]
y = df['monthly_bill']

print(f"Training samples: {len(X)}")
print(f"Features: {feature_cols}")

# Create pipeline with scaler and model
print("\nTraining model...")
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', LinearRegression())
])

pipeline.fit(X, y)

# Get model performance
train_score = pipeline.score(X, y)
print(f"✓ Model R² score: {train_score:.4f}")

# Save model with compatibility settings
print("\nSaving model...")
model_path = 'models/electricbills_predict.pkl'
joblib.dump(pipeline, model_path, compress=3, protocol=4)
print(f"✓ Saved to: {model_path}")

# Update metadata
metadata = {
    "training_date": datetime.now().isoformat(),
    "python_version": sys.version,
    "model_type": "LinearRegression",
    "n_features": len(feature_cols),
    "feature_names": feature_cols,
    "n_train_samples": len(X),
    "metrics": {
        "train_r2": float(train_score)
    },
    "coefficients": dict(zip(feature_cols, pipeline['regressor'].coef_)),
    "intercept": float(pipeline['regressor'].intercept_)
}

with open('models/model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("✓ Metadata saved")
print("=" * 60)
print("✅ Model retrained successfully for Streamlit Cloud deployment!")
print(f"   Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
print(f"   Pickle protocol: 4")
print(f"   Model R² score: {train_score:.4f}")
