import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def exploratory_analysis(input_path, output_dir):
    """Comprehensive EDA"""
    if not os.path.exists(input_path):
        print(f"Error: Processed data not found at {input_path}")
        return

    df = pd.read_csv(input_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Basic Statistics
    print("📊 Dataset Overview")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(df.describe())
    
    # 2. Distribution of Target
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    sns.histplot(df['energy_consumption_kwh'], bins=50, kde=True)
    plt.title('Distribution of Energy Consumption')
    plt.xlabel('kWh')
    
    plt.subplot(1, 2, 2)
    sns.boxplot(x=df['energy_consumption_kwh'])
    plt.title('Boxplot (Outliers check)')
    plt.savefig(os.path.join(output_dir, 'eda_target_distribution.png'))
    plt.close()
    
    # 3. Correlation Matrix
    plt.figure(figsize=(10, 8))
    correlation = df.corr()
    sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, fmt=".2f")
    plt.title('Feature Correlation Matrix')
    plt.savefig(os.path.join(output_dir, 'eda_correlation.png'))
    plt.close()
    
    # 4. Feature vs Target (Relationships)
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # household_size vs kWh (Boxplot mostly better for discrete values, but scatter for trend)
    sns.boxplot(x='household_size', y='energy_consumption_kwh', data=df, ax=axes[0, 0])
    axes[0, 0].set_title('Household Size vs kWh')
    
    # has_ac vs kWh (Boxplot)
    sns.boxplot(x='has_ac', y='energy_consumption_kwh', data=df, ax=axes[0, 1])
    axes[0, 1].set_title('AC vs kWh (0=No, 1=Yes)')
    
    # Season vs kWh
    # Need to reconstruct 'season' validation for pure graph 
    # (Checking raw features season_hot/rainy)
    # Let's just create a temporary column for viz
    def get_season_label(row):
        if row['season_hot'] == 1: return 'Hot'
        if row['season_rainy'] == 1: return 'Rainy'
        return 'Cool'
    
    df['season_label'] = df.apply(get_season_label, axis=1)
    sns.boxplot(x='season_label', y='energy_consumption_kwh', data=df, ax=axes[1, 0])
    axes[1, 0].set_title('Season vs kWh')
    
    # Weekend Ratio vs kWh (Scatter)
    sns.scatterplot(x='weekend_ratio', y='energy_consumption_kwh', data=df, alpha=0.3, ax=axes[1, 1])
    axes[1, 1].set_title('Weekend Ratio vs kWh')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'eda_feature_relationships.png'))
    plt.close()
    
    # 5. Key Insights
    print("\n🔍 Key Insights:")
    avg_kwh = df['energy_consumption_kwh'].mean()
    print(f"- Average Total consumption: {avg_kwh:.1f} kWh")
    
    with_ac = df[df['has_ac']==1]['energy_consumption_kwh'].mean()
    without_ac = df[df['has_ac']==0]['energy_consumption_kwh'].mean()
    print(f"- Avg With AC: {with_ac:.1f} kWh")
    print(f"- Avg Without AC: {without_ac:.1f} kWh")
    print(f"- AC Impact: +{with_ac - without_ac:.1f} kWh ({(with_ac - without_ac)/without_ac*100:.1f}%)")
    
    corr_size = df['household_size'].corr(df['energy_consumption_kwh'])
    print(f"- Correlation (Household Size vs kWh): {corr_size:.3f}")
    
    avg_hot = df[df['season_label']=='Hot']['energy_consumption_kwh'].mean()
    avg_cool = df[df['season_label']=='Cool']['energy_consumption_kwh'].mean()
    print(f"- Avg Hot Season: {avg_hot:.1f} kWh")
    print(f"- Avg Cool Season: {avg_cool:.1f} kWh")

if __name__ == "__main__":
    # Use the full combined processed data (we train on 'train' usually but for EDA full picture is nice)
    # But usually EDA is done on Train only to avoid bias! 
    # Let's stick to 'train.csv' for EDA to be proper.
    exploratory_analysis('data/processed/train.csv', 'outputs/eda')
