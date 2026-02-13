import kagglehub
import pandas as pd
import numpy as np
import os

# Download latest version (cached)
path = kagglehub.dataset_download("samxsam/household-energy-consumption")
csv_file = None
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".csv"):
            csv_file = os.path.join(root, file)
            break

print(f"Loading data from: {csv_file}")
df = pd.read_csv(csv_file)

# Standardize columns
df.columns = [c.strip().lower() for c in df.columns]

# Rename target if needed
if 'energy_consumption_kwh' not in df.columns:
     possible_targets = [c for c in df.columns if 'consumption' in c or 'kwh' in c]
     if possible_targets:
         df.rename(columns={possible_targets[0]: 'energy_consumption_kwh'}, inplace=True)

# ---------------------------------------------------------
# 1. Synthetic Date Generation (Fix for single-month data)
# ---------------------------------------------------------
print("Applying Synthetic Date Distribution (2025)...")

# Generate a range of dates for 2025
start_date = '2025-01-01'
end_date = '2025-12-31'
date_range = pd.date_range(start=start_date, end=end_date)

# Assign random dates from this range to the dataset
# We use numpy choice to sample with replacement
random_dates = np.random.choice(date_range, size=len(df))
df['date'] = random_dates

print("New Date Range:", df['date'].min(), "to", df['date'].max())

# ---------------------------------------------------------
# 2. validation
# ---------------------------------------------------------
# Clean data as before
if df['has_ac'].dtype == 'object':
    df['has_ac'] = df['has_ac'].map({'Yes': 1, 'No': 0, 'yes': 1, 'no': 0})

df = df[(df['household_size'].between(1, 20)) & (df['has_ac'].isin([0, 1]))]

# ---------------------------------------------------------
# 3. Feature Engineering
# ---------------------------------------------------------
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# Season Logic
def get_season(month):
    if month in [3, 4, 5, 6]:
        return 'hot'
    elif month in [7, 8, 9, 10]:
        return 'rainy'
    else:
        return 'cool'

df['season'] = df['month'].apply(get_season)
df['season_hot'] = (df['season'] == 'hot').astype(int)
df['season_rainy'] = (df['season'] == 'rainy').astype(int)

# Weekend Ratio Logic (Optimized)
unique_months = df[['year', 'month']].drop_duplicates()
ratio_lookup = {}

for _, row in unique_months.iterrows():
    days_in_month = pd.Period(f"{row['year']}-{row['month']}").days_in_month
    dates = pd.date_range(f"{row['year']}-{row['month']}-01", f"{row['year']}-{row['month']}-{days_in_month}")
    weekend_count = dates.dayofweek.isin([5, 6]).sum()
    ratio_lookup[(row['year'], row['month'])] = weekend_count / days_in_month

df['weekend_ratio'] = df.apply(lambda x: ratio_lookup[(x['year'], x['month'])], axis=1)

# Select final columns
final_cols = ['household_size', 'has_ac', 'season_hot', 'season_rainy', 'weekend_ratio', 'energy_consumption_kwh']
df_final = df[final_cols].copy()

# ---------------------------------------------------------
# 4. Split and Save
# ---------------------------------------------------------
from sklearn.model_selection import train_test_split
train, test = train_test_split(df_final, test_size=0.2, random_state=42)

os.makedirs('data/processed', exist_ok=True)
train.to_csv('data/processed/train.csv', index=False)
test.to_csv('data/processed/test.csv', index=False)

print(f"Saved processed data: {len(train)} train, {len(test)} test with SYNTHETIC DATES")
