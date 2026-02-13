
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score, mean_absolute_error

def visualize_model_performance():
    print("Generating Model Performance Visualizations...")
    
    # Load Data & Model
    try:
        test_df = pd.read_csv('data/processed/test.csv')
        model = joblib.load('models/electricbills_predict.pkl')
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    X_test = test_df.drop('energy_consumption_kwh', axis=1)
    y_test = test_df['energy_consumption_kwh']
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Metrics
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    output_dir = 'outputs/model_viz'
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Actual vs Predicted Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.3, color='blue', label='Data Points')
    
    # Perfect line y=x
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='Perfect Prediction')
    
    plt.xlabel('Actual kWh')
    plt.ylabel('Predicted kWh')
    plt.title(f'Actual vs Predicted (R2: {r2:.4f}, MAE: {mae:.2f})')
    plt.legend()
    plt.savefig(f'{output_dir}/actual_vs_predicted.png')
    plt.close()
    
    # 2. Residual Plot
    residuals = y_test - y_pred
    
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred, residuals, alpha=0.3, color='green')
    plt.axhline(y=0, color='red', linestyle='--')
    plt.xlabel('Predicted kWh')
    plt.ylabel('Residuals (Actual - Predicted)')
    plt.title('Residual Plot (Checking for patterns)')
    plt.savefig(f'{output_dir}/residual_plot.png')
    plt.close()
    
    # 3. Distribution of Residuals
    plt.figure(figsize=(10, 6))
    sns.histplot(residuals, bins=50, kde=True, color='purple')
    plt.title('Distribution of Residuals')
    plt.xlabel('Residual Value')
    plt.savefig(f'{output_dir}/residual_dist.png')
    plt.close()
    
    print(f"Visualizations saved to {output_dir}")

if __name__ == "__main__":
    visualize_model_performance()
