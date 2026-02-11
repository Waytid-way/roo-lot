import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib

def optimize_model():
    print("=" * 70)
    print("HYPERPARAMETER TUNING AND MODEL SELECTION")
    print("=" * 70)
    
    # Load Data
    df = pd.read_csv('data/electricity_data.csv')
    X = df[['ac_hours_per_day', 'num_appliances', 'room_area', 
            'ac_temperature', 'num_people']]
    y = df['electricity_bill']
    
    # Split and Scale
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Define models and parameters
    models = {
        'LinearRegression': {
            'model': LinearRegression(),
            'params': {}
        },
        'Ridge': {
            'model': Ridge(),
            'params': {'alpha': [0.1, 1.0, 10.0]}
        },
        'Lasso': {
            'model': Lasso(),
            'params': {'alpha': [0.1, 1.0, 10.0]}
        },
        'ElasticNet': {
            'model': ElasticNet(),
            'params': {'alpha': [0.1, 1.0, 10.0], 'l1_ratio': [0.1, 0.5, 0.9]}
        },
        'RandomForest': {
            'model': RandomForestRegressor(random_state=42),
            'params': {'n_estimators': [50, 100], 'max_depth': [None, 10, 20]}
        }
    }
    
    results = []
    best_overall_model = None
    best_overall_score = -np.inf
    best_model_name = ""
    
    print("\nStarting Grid Search...")
    print("-" * 70)
    
    for name, config in models.items():
        print(f"Tuning {name}...")
        grid = GridSearchCV(config['model'], config['params'], cv=5, scoring='r2', n_jobs=-1)
        grid.fit(X_train_scaled, y_train)
        
        best_model = grid.best_estimator_
        y_pred = best_model.predict(X_test_scaled)
        
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        print(f"  Best Params: {grid.best_params_}")
        print(f"  Test R2: {r2:.4f}")
        
        results.append({
            'Model': name,
            'Best_Params': str(grid.best_params_),
            'Test_R2': r2,
            'Test_MAE': mae,
            'Test_RMSE': rmse
        })
        
        if r2 > best_overall_score:
            best_overall_score = r2
            best_overall_model = best_model
            best_model_name = name
            
    # Save Results
    results_df = pd.DataFrame(results).sort_values('Test_R2', ascending=False)
    results_df.to_csv('outputs/model_comparison.csv', index=False)
    
    print("\n" + "=" * 70)
    print("MODEL COMPARISON RESULTS")
    print("=" * 70)
    print(results_df.to_string(index=False))
    
    print(f"\nBest Model: {best_model_name} (R2={best_overall_score:.4f})")
    
    # Save Best Model
    joblib.dump(best_overall_model, 'models/model_optimized.pkl')
    print("Saved optimized model to models/model_optimized.pkl")
    
    # Visualize Comparison
    plt.figure(figsize=(10, 6))
    
    # Add color array: highlight the best model
    colors = ['gray'] * len(results_df)
    colors[0] = 'green'  # Best model
    
    sns.barplot(data=results_df, x='Model', y='Test_R2', palette=colors)
    plt.title('Model Comparison (Test R2 Score)')
    plt.ylim(0, 1.0)
    plt.ylabel('R2 Score')
    plt.tight_layout()
    plt.savefig('outputs/model_comparison.png')
    print("Saved comparison chart to outputs/model_comparison.png")

if __name__ == "__main__":
    optimize_model()
