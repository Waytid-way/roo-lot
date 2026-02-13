"""
Check model file information and Python version compatibility
"""
import os
import sys
import pickle
import joblib
from pathlib import Path

print(f"Current Python Version: {sys.version}")
print(f"Python Version Info: {sys.version_info}")
print("-" * 60)

model_path = Path("models/electricbills_predict.pkl")

if model_path.exists():
    print(f"✓ Model file exists: {model_path}")
    print(f"  File size: {model_path.stat().st_size / 1024:.2f} KB")
    print(f"  Last modified: {model_path.stat().st_mtime}")
    print("-" * 60)
    
    # Try to load the model
    try:
        print("Attempting to load model...")
        model = joblib.load(model_path)
        print("✓ Model loaded successfully!")
        print(f"  Model type: {type(model)}")
        print(f"  Model: {model}")
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        print(f"  Error type: {type(e).__name__}")
        
        # Try to read pickle protocol version
        try:
            with open(model_path, 'rb') as f:
                protocol = pickle.load(f).__reduce_ex__(4)
                print(f"  Pickle info: {protocol}")
        except Exception as e2:
            print(f"  Could not determine pickle protocol: {e2}")
else:
    print(f"✗ Model file NOT FOUND: {model_path}")

print("-" * 60)
print("\n📋 All model files:")
models_dir = Path("models")
for pkl_file in models_dir.glob("*.pkl"):
    size_kb = pkl_file.stat().st_size / 1024
    print(f"  - {pkl_file.name}: {size_kb:.2f} KB")
