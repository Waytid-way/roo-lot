import pandas as pd
import numpy as np
import os

def create_template():
    """Create data collection template"""
    template = pd.DataFrame({
        'ac_hours_per_day': [8.0, 6.0, 10.0, 0.0, 4.0],
        'num_appliances': [5, 4, 7, 3, 5],
        'room_area': [25.0, 20.0, 35.0, 18.0, 28.0],
        'ac_temperature': [25.0, 26.0, 24.0, 0.0, 27.0],
        'num_people': [1, 1, 2, 1, 2],
        'electricity_bill': [850, 650, 1200, 350, 720]
    })
    os.makedirs('data', exist_ok=True)
    template.to_csv('data/electricity_data_template.csv', index=False)
    print("Template created: data/electricity_data_template.csv")

def validate_electricity_data(df):
    """Validate electricity dataset"""
    errors = []
    warnings = []
    
    # Required columns
    required_cols = ['ac_hours_per_day', 'num_appliances', 'room_area', 
                     'ac_temperature', 'num_people', 'electricity_bill']
    
    missing_cols = set(required_cols) - set(df.columns)
    if missing_cols:
        errors.append(f"Missing columns: {missing_cols}")
        return errors, warnings
    
    # Check data types
    if not pd.api.types.is_numeric_dtype(df['ac_hours_per_day']):
        errors.append("ac_hours_per_day must be numeric")
    
    # Range validations
    if (df['ac_hours_per_day'] < 0).any() or (df['ac_hours_per_day'] > 24).any():
        errors.append("ac_hours_per_day must be between 0-24")
    
    if (df['num_appliances'] < 0).any():
        errors.append("num_appliances must be >= 0")
    
    if (df['room_area'] <= 0).any():
        errors.append("room_area must be > 0")
    
    if (df['ac_temperature'] < 0).any() or (df['ac_temperature'] > 35).any():
        errors.append("ac_temperature must be between 0-35 deg C")
    
    if (df['num_people'] < 1).any():
        errors.append("num_people must be >= 1")
    
    if (df['electricity_bill'] < 0).any():
        errors.append("electricity_bill must be >= 0")
    
    # Check for missing values
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        warnings.append(f"Found {missing_count} missing values")
    
    # Check sample size
    if len(df) < 30:
        warnings.append(f"Sample size ({len(df)}) is small. Recommend >= 50 samples")
    
    # Outlier detection (simple IQR method)
    for col in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
        if outliers > 0:
            warnings.append(f"{col}: {outliers} potential outliers detected")
    
    return errors, warnings

def generate_sample_data(n_samples=100, seed=42):
    """Generate synthetic electricity data"""
    np.random.seed(seed)
    
    data = {
        'ac_hours_per_day': np.random.uniform(0, 14, n_samples),
        'num_appliances': np.random.randint(2, 10, n_samples),
        'room_area': np.random.uniform(15, 45, n_samples),
        'ac_temperature': np.random.choice([0] + list(range(22, 29)), n_samples),
        'num_people': np.random.randint(1, 4, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Generate realistic electricity bill
    # Formula: base + AC cost + appliances + area factor
    df['electricity_bill'] = (
        200 +  # Base cost
        df['ac_hours_per_day'] * 30 * 5 +  # AC cost
        df['num_appliances'] * 20 +  # Appliance cost
        df['room_area'] * 2 +  # Area factor
        (30 - df['ac_temperature']) * 15 +  # Temperature effect
        df['num_people'] * 50 +  # People factor
        np.random.normal(0, 50, n_samples)  # Random noise
    ).clip(lower=100)
    
    df['electricity_bill'] = df['electricity_bill'].round(2)
    
    return df

if __name__ == "__main__":
    # 1. Create Template
    create_template()
    
    # 2. Generate Sample Data
    print("\nGenerating sample data...")
    sample_df = generate_sample_data(100)
    sample_df.to_csv('data/electricity_data_sample.csv', index=False)
    # Also save as main data file for next steps
    sample_df.to_csv('data/electricity_data.csv', index=False)
    print("Generated 100 sample records -> data/electricity_data_sample.csv")
    print("Also saved as -> data/electricity_data.csv")

    # 3. Validate Data
    print("\nValidating data...")
    df = pd.read_csv('data/electricity_data.csv')
    errors, warnings = validate_electricity_data(df)
    
    print("=" * 50)
    print("DATA VALIDATION REPORT")
    print("=" * 50)
    print(f"Total Rows: {len(df)}")
    print(f"Total Columns: {len(df.columns)}")
    
    if errors:
        print("\nERRORS:")
        for err in errors:
            print(f"  - {err}")
    else:
        print("\nNo errors found!")
    
    if warnings:
        print("\nWARNINGS:")
        for warn in warnings:
            print(f"  - {warn}")
    else:
        print("\nNo warnings!")
    
    # Summary statistics
    print("\n" + "=" * 50)
    print("SUMMARY STATISTICS")
    print("=" * 50)
    print(df.describe())
