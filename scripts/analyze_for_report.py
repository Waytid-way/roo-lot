"""
วิเคราะห์ข้อมูลสำหรับเขียน Report
"""
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('data/processed/train.csv')

print("=" * 80)
print("📊 DATASET STATISTICS FOR REPORT")
print("=" * 80)

# Basic Statistics
print("\n1. BASIC STATISTICS")
print("-" * 80)
print(df.describe())

# Correlation Analysis
print("\n\n2. CORRELATION WITH TARGET (energy_consumption_kwh)")
print("-" * 80)
corr_with_target = df.corr()['energy_consumption_kwh'].sort_values(ascending=False)
print(corr_with_target)

# AC Impact
print("\n\n3. AIR CONDITIONER IMPACT ANALYSIS")
print("-" * 80)
with_ac = df[df['has_ac'] == 1]['energy_consumption_kwh'].mean()
without_ac = df[df['has_ac'] == 0]['energy_consumption_kwh'].mean()
difference = with_ac - without_ac
percentage = (difference / without_ac) * 100

print(f"Average consumption WITH AC:     {with_ac:.2f} kWh")
print(f"Average consumption WITHOUT AC:  {without_ac:.2f} kWh")
print(f"Absolute difference:             +{difference:.2f} kWh")
print(f"Percentage increase:             +{percentage:.1f}%")

# Household Size Impact
print("\n\n4. HOUSEHOLD SIZE IMPACT ANALYSIS")
print("-" * 80)
household_analysis = df.groupby('household_size')['energy_consumption_kwh'].agg([
    ('Mean (kWh)', 'mean'),
    ('Std Dev', 'std'),
    ('Min', 'min'),
    ('Max', 'max'),
    ('Count', 'count')
])
print(household_analysis)

# Seasonal Impact
print("\n\n5. SEASONAL IMPACT ANALYSIS")
print("-" * 80)
df['season'] = 'Cool'
df.loc[df['season_hot'] == 1, 'season'] = 'Hot'
df.loc[df['season_rainy'] == 1, 'season'] = 'Rainy'

seasonal_analysis = df.groupby('season')['energy_consumption_kwh'].agg([
    ('Mean (kWh)', 'mean'),
    ('Std Dev', 'std'),
    ('Count', 'count')
])
print(seasonal_analysis)

# Distribution Analysis
print("\n\n6. DISTRIBUTION ANALYSIS")
print("-" * 80)
print(f"Minimum consumption:      {df['energy_consumption_kwh'].min():.2f} kWh")
print(f"25th Percentile (Q1):     {df['energy_consumption_kwh'].quantile(0.25):.2f} kWh")
print(f"Median (50th Percentile): {df['energy_consumption_kwh'].median():.2f} kWh")
print(f"75th Percentile (Q3):     {df['energy_consumption_kwh'].quantile(0.75):.2f} kWh")
print(f"Maximum consumption:      {df['energy_consumption_kwh'].max():.2f} kWh")
print(f"Mean:                     {df['energy_consumption_kwh'].mean():.2f} kWh")
print(f"Standard Deviation:       {df['energy_consumption_kwh'].std():.2f} kWh")
print(f"Skewness:                 {df['energy_consumption_kwh'].skew():.2f}")
print(f"Kurtosis:                 {df['energy_consumption_kwh'].kurtosis():.2f}")

# Weekend Ratio Analysis
print("\n\n7. WEEKEND RATIO IMPACT")
print("-" * 80)
print(f"Correlation with consumption: {df['weekend_ratio'].corr(df['energy_consumption_kwh']):.4f}")
print(f"Min weekend ratio: {df['weekend_ratio'].min():.4f}")
print(f"Max weekend ratio: {df['weekend_ratio'].max():.4f}")
print(f"Mean weekend ratio: {df['weekend_ratio'].mean():.4f}")

print("\n" + "=" * 80)
print("✅ Analysis complete!")
print("=" * 80)
