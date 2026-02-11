import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import (r2_score, mean_absolute_error, 
                            mean_squared_error, mean_absolute_percentage_error)
import joblib

def evaluate_model():
    print("=" * 70)
    print("MODEL EVALUATION REPORT")
    print("=" * 70)

    # Load model and data
    try:
        model = joblib.load('models/model.pkl')
        scaler = joblib.load('models/scaler.pkl')
        df = pd.read_csv('data/electricity_data.csv')
    except FileNotFoundError:
        print("Error: Models or data not found. Run previous steps first.")
        return

    # Prepare data
    X = df[['ac_hours_per_day', 'num_appliances', 'room_area', 
            'ac_temperature', 'num_people']]
    y = df['electricity_bill']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Predictions
    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)

    # 1. Regression Metrics
    print("\n1. REGRESSION METRICS")
    print("-" * 70)

    metrics = {
        'R2 Score': [r2_score(y_train, y_train_pred), r2_score(y_test, y_test_pred)],
        'MAE': [mean_absolute_error(y_train, y_train_pred), 
                mean_absolute_error(y_test, y_test_pred)],
        'RMSE': [np.sqrt(mean_squared_error(y_train, y_train_pred)), 
                 np.sqrt(mean_squared_error(y_test, y_test_pred))],
        'MAPE (%)': [mean_absolute_percentage_error(y_train, y_train_pred) * 100,
                     mean_absolute_percentage_error(y_test, y_test_pred) * 100]
    }

    metrics_df = pd.DataFrame(metrics, index=['Train', 'Test'])
    print(metrics_df.round(4))

    # 2. Residual Analysis
    print("\n2. RESIDUAL ANALYSIS")
    print("-" * 70)
    
    residuals = y_test - y_test_pred
    print(f"Mean Residual: {residuals.mean():.4f}")
    print(f"Std Residual: {residuals.std():.4f}")
    
    # 3. Visualization
    print("\nGenerating evaluation plots...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Actual vs Predicted
    axes[0, 0].scatter(y_test, y_test_pred, alpha=0.6, color='blue')
    axes[0, 0].plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    axes[0, 0].set_xlabel('Actual Bill')
    axes[0, 0].set_ylabel('Predicted Bill')
    axes[0, 0].set_title('Actual vs Predicted (Test Set)')
    
    # Plot 2: Residuals Distribution
    sns.histplot(residuals, kde=True, ax=axes[0, 1], color='green')
    axes[0, 1].set_xlabel('Residuals')
    axes[0, 1].set_title('Residuals Distribution')
    
    # Plot 3: Residuals vs Predicted
    axes[1, 0].scatter(y_test_pred, residuals, alpha=0.6, color='purple')
    axes[1, 0].axhline(y=0, color='r', linestyle='--')
    axes[1, 0].set_xlabel('Predicted Bill')
    axes[1, 0].set_ylabel('Residuals')
    axes[1, 0].set_title('Residuals vs Predicted')
    
    # Plot 4: Feature Importance (Coefficients)
    coef_df = pd.DataFrame({
        'Feature': X.columns,
        'Coefficient': model.coef_
    }).sort_values('Coefficient', key=abs, ascending=False)
    
    sns.barplot(data=coef_df, x='Coefficient', y='Feature', ax=axes[1, 1], palette='viridis')
    axes[1, 1].set_title('Feature Importance (Standardized Coefficients)')
    
    plt.tight_layout()
    plt.savefig('outputs/model_evaluation.png', dpi=300)
    print("Saved: outputs/model_evaluation.png")
    
    # Save Report
    report = f"""MODEL EVALUATION REPORT
Generated: {pd.Timestamp.now()}

METRICS SUMMARY
--------------------------------------------------
{metrics_df.to_string()}

RESIDUAL ANALYSIS
--------------------------------------------------
Mean Residual: {residuals.mean():.4f}
Std Residual: {residuals.std():.4f}

FILES GENERATED
--------------------------------------------------
- outputs/model_evaluation.png
"""
    
    with open('outputs/evaluation_report.txt', 'w') as f:
        f.write(report)
        
    print("\nEVALUATION COMPLETE")
    print("Report saved to outputs/evaluation_report.txt")

if __name__ == "__main__":
    evaluate_model()
