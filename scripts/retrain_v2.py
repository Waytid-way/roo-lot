
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import os
import sys

# Ensure output directories exist
os.makedirs("models", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("data/real_v2", exist_ok=True)

# File paths
DATA_PATH = r"C:\Users\com\Documents\AIE322\RooLord\roo-lot\data\electric_price - Sheet1.csv"
MODEL_PATH = "models/model_v2_next_month.pkl"
REPORT_PATH = "outputs/real_data_v2_report.md"

def load_data(filepath):
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    return df

def clean_data(df):
    print("Cleaning data...")
    
    # Fill missing people values based on note
    # If note contains "ปิดเทอม" -> fill with 0
    # If note is empty but people is NaN -> fill with 2
    
    # Create mask for "ปิดเทอม" in note
    # Handle NaN in note first
    df['note'] = df['note'].fillna('')
    
    mask_break = df['note'].str.contains("ปิดเทอม", na=False)
    
    # Apply logic
    df.loc[mask_break & df['people'].isna(), 'people'] = 0
    df['people'] = df['people'].fillna(2)
    
    # Convert date to datetime
    # The format in CSV preview was 11/1/2023 (M/D/Y likely)
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y', errors='coerce')
    
    # Check for any failures in date conversion
    if df['date'].isna().any():
        print("Warning: Some dates could not be parsed.")
        
    df = df.sort_values('date').reset_index(drop=True)
    return df

def feature_engineering(df):
    print("Feature Engineering...")
    
    # Create Target: Next Month Bill (shift -1)
    df['target_next_bill'] = df['electric_price'].shift(-1)
    
    # Current Bill & Units
    df['current_bill'] = df['electric_price']
    df['current_unit'] = df['amount(unit)']
    
    # Lag Features
    df['lag1_unit'] = df['amount(unit)'].shift(1)
    df['lag2_unit'] = df['amount(unit)'].shift(2)
    
    # Is Break
    df['is_break'] = df['note'].str.contains("ปิดเทอม", na=False).astype(int)
    
    # Month
    df['month'] = df['date'].dt.month
    
    # Ensure people is numeric
    df['people'] = pd.to_numeric(df['people'])
    
    # Drop rows with NaN (due to lags and target shift)
    # Target shift creates NaN at the end. Lag shift creates NaN at the start.
    df_clean = df.dropna().reset_index(drop=True)
    
    return df_clean

def select_features(df):
    print("Feature Selection...")
    
    # Candidates
    candidates = ['current_bill', 'current_unit', 'lag1_unit', 'lag2_unit', 'is_break', 'month', 'people']
    
    # Compute correlation with target
    correlations = df[candidates + ['target_next_bill']].corr()['target_next_bill'].drop('target_next_bill')
    print("\nCorrelations with Target:")
    print(correlations.sort_values(ascending=False))
    
    # Selection logic based on prompt
    # Priority 1: current_unit OR current_bill
    # Priority 2: is_break
    # Priority 3: month
    # Priority 4: people
    
    # Check correlation between current_bill and current_unit
    corr_bill_unit = df['current_bill'].corr(df['current_unit'])
    print(f"\nCorrelation between current_bill and current_unit: {corr_bill_unit}")
    
    selected_features = []
    
    # Pick one of current_bill or current_unit
    if abs(correlations['current_unit']) >= abs(correlations['current_bill']):
        selected_features.append('current_unit')
    else:
        selected_features.append('current_bill')
        
    selected_features.append('is_break')
    selected_features.append('month')
    selected_features.append('people')
    
    # Add lag1_unit if meaningful? Prompt says "Select Top 5 Features"
    # But list only has 4 priorities. I will add lag1_unit as 5th if not already there.
    if 'lag1_unit' not in selected_features:
        selected_features.append('lag1_unit')
        
    print(f"\nSelected Features: {selected_features}")
    return selected_features

def train_model(df, features):
    print("Training Model...")
    
    X = df[features]
    y = df['target_next_bill']
    
    # Time Series Split (80/20) - No Shuffle
    split_idx = int(len(df) * 0.8)
    
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
    
    # Model: Ridge Regression
    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)
    
    # Preds
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Metrics
    mae_test = mean_absolute_error(y_test, y_pred_test)
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
    
    mae_train = mean_absolute_error(y_train, y_pred_train)
    rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
    
    print(f"\nModel Performance (Test Set):")
    print(f"MAE: {mae_test:.2f}")
    print(f"RMSE: {rmse_test:.2f}")
    
    return model, X_test, y_test, y_pred_test, mae_test, rmse_test

def generate_report(model, features, mae, rmse, df_test, y_pred):
    print("Generating Report...")
    
    report_content = f"""# Real Data V2 Retraining Report

## Model Performance
- **Model:** Ridge Regression
- **Features:** {features}
- **MAE (Test):** {mae:.2f}
- **RMSE (Test):** {rmse:.2f}

## Feature Coefficients
"""
    for feat, coef in zip(features, model.coef_):
        report_content += f"- **{feat}:** {coef:.4f}\n"

    report_content += "\n## Test Data Predictions\n"
    report_content += "| Date | Actual Next Bill | Predicted Next Bill | Error |\n"
    report_content += "|---|---|---|---|\n"
    
    # We need dates for the test set. 
    # The df passed to train_model was split. Converting to list ensures alignment is tricky if we don't have the index.
    # But X_test has the index.
    
    # We can reconstruct a DF for the report
    results = df_test.copy()
    results['Predicted'] = y_pred
    results['Actual'] = results['target_next_bill'] # Assuming this column exists in X_test? No, X_test is features only.
    # Wait, df_test passed to this function needs to be the full dataframe slice or I need to pass y_test separately.
    # I passed X_test, y_test, y_pred_test to this function? No, looking at signature:
    # generate_report(model, features, mae, rmse, df_test, y_pred)
    # I will adjust the call site to pass a dataframe that has dates.
    
    return report_content

def main():
    # 1. Load
    try:
        df = load_data(DATA_PATH)
    except FileNotFoundError:
        print(f"Error: File not found at {DATA_PATH}")
        return

    # 2. Clean
    df = clean_data(df)
    
    # 3. Feature Engineering
    df = feature_engineering(df)
    print(f"Data after processing: {len(df)} rows")
    print(df.head())
    
    # 4. Feature Selection
    features = select_features(df)
    
    # 5. Train
    model, X_test, y_test, y_pred_test, mae, rmse = train_model(df, features)
    
    # 6. Save Model
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    
    # 7. Generate Report
    # Join X_test with original date if possible, or just use indices
    # We want to see dates in the report.
    # X_test preserves the index from df.
    test_dates = df.loc[X_test.index, 'date']
    
    report = f"""# Real Data V2 Retraining Report

## Model Performance
- **Model:** Ridge Regression
- **Features:** {features}
- **MAE (Test):** {mae:.2f}
- **RMSE (Test):** {rmse:.2f}
- **Intercept:** {model.intercept_:.2f}

## Feature Coefficients
"""
    for feat, coef in zip(features, model.coef_):
        report += f"- **{feat}:** {coef:.4f}\n"
    
    report += "\n## Test Set Predictions\n"
    report += "| Date | Actual | Predicted | Error |\n"
    report += "|---|---|---|---|\n"
    
    for date, actual, pred in zip(test_dates, y_test, y_pred_test):
        error = actual - pred
        report += f"| {date.strftime('%Y-%m-%d')} | {actual:.2f} | {pred:.2f} | {error:.2f} |\n"
        
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"Report saved to {REPORT_PATH}")
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(test_dates, y_test, label='Actual Next Month Bill', marker='o')
    plt.plot(test_dates, y_pred_test, label='Predicted Next Month Bill', marker='x', linestyle='--')
    plt.title('Actual vs Predicted Electricity Bill (Test Set)')
    plt.xlabel('Date')
    plt.ylabel('Bill Amount')
    plt.legend()
    plt.grid(True)
    plt.savefig('outputs/prediction_plot.png')
    print("Plot saved to outputs/prediction_plot.png")

if __name__ == "__main__":
    main()
