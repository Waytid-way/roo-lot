import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

def train_and_compare_models():
    print("=" * 70)
    print("PHASE 2: MODEL TRAINING & SELECTION")
    print("=" * 70)

    # 1. Load Data
    train_path = 'data/processed/train.csv'
    test_path = 'data/processed/test.csv'
    
    if not os.path.exists(train_path):
        print("Error: Train data not found!")
        return

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    X_train = train_df.drop('energy_consumption_kwh', axis=1)
    y_train = train_df['energy_consumption_kwh']
    
    X_test = test_df.drop('energy_consumption_kwh', axis=1)
    y_test = test_df['energy_consumption_kwh']
    
    print(f"Train size: {X_train.shape}, Test size: {X_test.shape}")
    print(f"Features: {X_train.columns.tolist()}")

    # 2. Define Models and Params
    models = {
        'Linear Regression': {
            'model': LinearRegression(),
            'params': {}
        },
        'Ridge': {
            'model': Ridge(),
            'params': {'reg__alpha': [0.01, 0.1, 1.0, 10.0, 100.0]}
        },
        'Lasso': {
            'model': Lasso(),
            'params': {'reg__alpha': [0.001, 0.01, 0.1, 1.0, 10.0]}
        },
        'Random Forest': {
            'model': RandomForestRegressor(random_state=42),
            'params': {
                'reg__n_estimators': [50, 100], 
                'reg__max_depth': [10, 20, None],
                'reg__min_samples_split': [2, 5]
            }
        }
    }

    results = []
    best_model_obj = None
    best_score = -np.inf
    best_model_name = ""
    
    # 3. Training Loop
    validation_df = pd.DataFrame(columns=['Model', 'Best Params', 'CV R2', 'Test R2', 'MAE', 'RMSE'])

    for name, config in models.items():
        print(f"\nTraining {name}...")
        
        # Create Pipeline
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('reg', config['model'])
        ])
        
        # Grid Search
        # Note: 'reg__' prefix is needed because model is inside pipeline step 'reg'
        grid = GridSearchCV(
            pipeline, 
            config['params'], 
            cv=5, 
            scoring='r2', 
            n_jobs=-1,
            verbose=1
        )
        
        grid.fit(X_train, y_train)
        
        # Evaluation
        best_estimator = grid.best_estimator_
        y_pred = best_estimator.predict(X_test)
        
        test_r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        print(f"  Best Params: {grid.best_params_}")
        print(f"  CV R2: {grid.best_score_:.4f}")
        print(f"  Test R2: {test_r2:.4f}")
        print(f"  MAE: {mae:.4f}")
        
        # Store results
        results.append({
            'Model': name,
            'Best Params': str(grid.best_params_),
            'CV R2': grid.best_score_,
            'Test R2': test_r2,
            'MAE': mae,
            'RMSE': rmse,
            'Object': best_estimator
        })
        
        # Track best model (based on Test R2)
        if test_r2 > best_score:
            best_score = test_r2
            best_model_obj = best_estimator
            best_model_name = name

    # 4. Comparison Table
    results_df = pd.DataFrame(results).drop('Object', axis=1)
    results_df = results_df.sort_values('Test R2', ascending=False)
    
    print("\n" + "=" * 70)
    print("MODEL COMPARISON RESULTS")
    print("=" * 70)
    print(results_df)

    print(f"\n🏆 Winner: {best_model_name} (R2: {best_score:.4f})")

    # 5. Save Best Model
    os.makedirs('models', exist_ok=True)
    
    # Save the full pipeline (includes scaler!)
    joblib.dump(best_model_obj, 'models/electricbills_predict.pkl')
    
    # Save scaler separately just in case (though it's in the pipeline)
    # Access scaler from pipeline
    scaler = best_model_obj.named_steps['scaler']
    joblib.dump(scaler, 'models/scaler.pkl')
    
    print(f"Saved model to models/electricbills_predict.pkl")

    # 6. Feature Importance (if applicable)
    if best_model_name in ['Linear Regression', 'Ridge', 'Lasso']:
        model = best_model_obj.named_steps['reg']
        coefs = pd.DataFrame({
            'Feature': X_train.columns,
            'Coefficient': model.coef_
        }).sort_values('Coefficient', ascending=False)
        print("\nFeature Importance (Coefficients):")
        print(coefs)
    elif best_model_name == 'Random Forest':
        model = best_model_obj.named_steps['reg']
        imps = pd.DataFrame({
            'Feature': X_train.columns,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)
        print("\nFeature Importance:")
        print(imps)

if __name__ == "__main__":
    train_and_compare_models()
