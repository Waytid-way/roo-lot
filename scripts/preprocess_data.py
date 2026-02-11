import pandas as pd
import numpy as np
import os
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from scipy import stats

def preprocess_data():
    """Clean and preprocess electricity data"""
    # Load data
    df = pd.read_csv('data/electricity_data.csv')
    print("=" * 50)
    print("DATA DATA PREPROCESSING")
    print("=" * 50)
    
    print("Missing Values Before:")
    print(df.isnull().sum())
    
    # Strategy 1: Fill numeric missing values with median
    imputer = SimpleImputer(strategy='median')
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
    
    # Strategy 2: Drop rows with too many missing values
    threshold = 0.5
    df = df.dropna(thresh=int(threshold * len(df.columns)))
    
    # Outlier Removal (IQR)
    print("\nOUTLIER REMOVAL (IQR Method)")
    print("-" * 30)
    df_clean = df.copy()
    outliers_removed = 0
    
    target_cols = ['ac_hours_per_day', 'num_appliances', 'room_area', 
                   'ac_temperature', 'electricity_bill']
    
    for col in target_cols:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        before = len(df_clean)
        df_clean = df_clean[(df_clean[col] >= lower_bound) & 
                           (df_clean[col] <= upper_bound)]
        after = len(df_clean)
        removed = before - after
        
        if removed > 0:
            print(f"  {col}: Removed {removed} outliers")
            outliers_removed += removed
            
    print(f"\nTotal outliers removed: {outliers_removed}")
    print(f"Dataset size: {len(df)} -> {len(df_clean)}")
    
    # Feature Scaling
    print("\nFEATURE SCALING (StandardScaler)")
    print("-" * 30)
    
    # Separate features and target
    X = df_clean[['ac_hours_per_day', 'num_appliances', 'room_area', 
                  'ac_temperature', 'num_people']]
    y = df_clean['electricity_bill']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
    
    print("Original Scale:")
    print(X.describe().loc[['mean', 'std']])
    print("\nScaled (mean=0, std=1):")
    print(X_scaled_df.describe().loc[['mean', 'std']])
    
    # Save processed data
    # Combine scaled features with target
    df_processed = X_scaled_df.copy()
    df_processed['electricity_bill'] = y.values
    
    df_processed.to_csv('data/electricity_data_processed.csv', index=False)
    
    # Generate report
    report = f"""DATA PREPROCESSING REPORT
Generated: {pd.Timestamp.now()}

ORIGINAL DATA:
- Total samples: {len(df)}
- Features: {len(df.columns) - 1}

CLEANING STEPS:
1. Missing values filled with median
2. Outliers removed using IQR method (threshold=1.5)
3. Features scaled using StandardScaler

PROCESSED DATA:
- Total samples: {len(df_processed)}
- Samples removed: {len(df) - len(df_processed)} ({(len(df) - len(df_processed))/len(df)*100:.2f}%)

FILES CREATED:
- data/electricity_data_processed.csv
"""
    with open('data/preprocessing_report.txt', 'w') as f:
        f.write(report)
        
    print("\nPREPROCESSING COMPLETE")
    print("Report saved to data/preprocessing_report.txt")

if __name__ == "__main__":
    preprocess_data()
