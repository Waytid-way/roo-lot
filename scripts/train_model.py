import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
from datetime import datetime
import json
import os

def train_model():
    print("=" * 70)
    print("MODEL TRAINING PIPELINE")
    print("=" * 70)

    # Step 1: Load Data
    # We use the processed data from Skill 2
    if not os.path.exists('data/electricity_data_processed.csv'):
        print("Error: Processed data file not found. Run scripts/preprocess_data.py first.")
        return

    df = pd.read_csv('data/electricity_data_processed.csv')
    print(f"\nLoaded {len(df)} samples")

    # Step 2: Prepare Features and Target
    X = df[['ac_hours_per_day', 'num_appliances', 'room_area', 
            'ac_temperature', 'num_people']]
    y = df['electricity_bill']

    print(f"Features: {list(X.columns)}")
    print(f"Target: electricity_bill")

    # Step 3: Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"\nTrain samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")

    # Step 4: Feature Scaling
    # Note: Data was already scaled in preprocessing, but usually we fit scaler on train
    # and transform test to avoid leakage. 
    # However, let's re-do it properly here to ensure we have the scaler object to save.
    # We will reload the original CSV or just recognize that the processed one is already scaled.
    # WAIT: The processed file has EVERYTHING scaled. This is slightly incorrect for a real pipeline
    # because of data leakage (scaling before split). 
    # Let's fix this: Load the RAW data, clean it, split, THEN scale.
    # Or, to follow the skill check exactly, I should load the raw data again? 
    # The skill says "Load electricity_data.csv" (line 591 of Agent_Skills). 
    # Okay, I will load the RAW data and do the pipeline properly here.
    
    df_raw = pd.read_csv('data/electricity_data.csv')
    
    # Simple cleaning (handling outliers was done in preprocessing, but for training pipeline we need robust scaling)
    # For simplicity and consistency with the skill which loads 'electricity_data.csv' (line 591):
    
    X_raw = df_raw[['ac_hours_per_day', 'num_appliances', 'room_area', 
            'ac_temperature', 'num_people']]
    y_raw = df_raw['electricity_bill']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_raw, y_raw, test_size=0.2, random_state=42
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("\nFeatures scaled (StandardScaler)")

    # Step 5: Train Model
    print("\n" + "=" * 70)
    print("TRAINING MODEL...")
    print("=" * 70)

    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    print("Model trained successfully")

    # Step 6: Cross-Validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, 
                                cv=5, scoring='r2')

    print(f"\n5-Fold Cross-Validation R2 Scores:")
    for i, score in enumerate(cv_scores, 1):
        print(f"  Fold {i}: {score:.4f}")
    print(f"  Mean: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

    # Step 7: Predictions
    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)

    # Step 8: Calculate Metrics
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

    print("\n" + "=" * 70)
    print("MODEL PERFORMANCE")
    print("=" * 70)
    print("\nTraining Set:")
    print(f"  R2 Score: {train_r2:.4f}")
    print(f"  MAE: {train_mae:.2f}")
    print(f"  RMSE: {train_rmse:.2f}")

    print("\nTest Set:")
    print(f"  R2 Score: {test_r2:.4f}")
    print(f"  MAE: {test_mae:.2f}")
    print(f"  RMSE: {test_rmse:.2f}")

    # Check for overfitting
    if train_r2 - test_r2 > 0.1:
        print("\nWarning: Possible overfitting detected")
    else:
        print("\nNo significant overfitting")

    # Step 9: Feature Coefficients
    print("\n" + "=" * 70)
    print("FEATURE IMPORTANCE (Coefficients)")
    print("=" * 70)

    coefficients = pd.DataFrame({
        'Feature': X.columns,
        'Coefficient': model.coef_,
        'Abs_Coefficient': np.abs(model.coef_)
    }).sort_values('Abs_Coefficient', ascending=False)

    print(coefficients.to_string(index=False))

    # Step 10: Save Model and Artifacts
    os.makedirs('models', exist_ok=True)

    joblib.dump(model, 'models/model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')

    # Save metadata
    metadata = {
        'training_date': datetime.now().isoformat(),
        'model_type': 'LinearRegression',
        'n_features': len(X.columns),
        'feature_names': list(X.columns),
        'n_train_samples': len(X_train),
        'n_test_samples': len(X_test),
        'metrics': {
            'train_r2': float(train_r2),
            'test_r2': float(test_r2),
            'train_mae': float(train_mae),
            'test_mae': float(test_mae),
            'train_rmse': float(train_rmse),
            'test_rmse': float(test_rmse),
            'cv_mean_r2': float(cv_scores.mean()),
            'cv_std_r2': float(cv_scores.std())
        },
        'coefficients': {feat: float(coef) for feat, coef in zip(X.columns, model.coef_)},
        'intercept': float(model.intercept_)
    }

    with open('models/model_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)

    print("\n" + "=" * 70)
    print("MODEL SAVED SUCCESSFULLY")
    print("=" * 70)
    print("Files created:")
    print("  - models/model.pkl")
    print("  - models/scaler.pkl")
    print("  - models/model_metadata.json")

if __name__ == "__main__":
    train_model()
