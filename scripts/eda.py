import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def run_eda():
    """Run Exploratory Data Analysis"""
    print("=" * 70)
    print("EXPLORATORY DATA ANALYSIS - ELECTRICITY BILL PREDICTION")
    print("=" * 70)
    
    # Load data
    df = pd.read_csv('data/electricity_data.csv')
    
    insights = []
    
    # 1. Dataset Overview
    print("\n1. DATASET OVERVIEW")
    print("-" * 70)
    print(f"Shape: {df.shape} (rows, columns)")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    print("\nData Types:")
    print(df.dtypes)
    
    insights.append("DATASET OVERVIEW")
    insights.append(f"Shape: {df.shape}")
    insights.append("-" * 30)
    
    # 2. Statistical Summary
    print("\n2. STATISTICAL SUMMARY")
    print("-" * 70)
    print(df.describe())
    
    # 3. Missing Values
    print("\n3. MISSING VALUES")
    print("-" * 70)
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("No missing values")
    else:
        print(missing[missing > 0])
        
    # 4. Correlation Analysis
    print("\n4. CORRELATION ANALYSIS")
    print("-" * 70)
    df_numeric = df.select_dtypes(include=[np.number])
    correlation = df_numeric.corr()
    print("\nCorrelation with Target (electricity_bill):")
    corr_with_target = correlation['electricity_bill'].sort_values(ascending=False)
    print(corr_with_target)
    
    # Visualization 1: Correlation Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, fmt='.3f', cmap='coolwarm', 
                center=0, square=True, linewidths=1)
    plt.title('Feature Correlation Matrix', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('outputs/correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("Saved: outputs/correlation_heatmap.png")
    plt.close()
    
    # Visualization 2: Distribution Plots
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for idx, col in enumerate(df.columns):
        if idx < len(axes):
            sns.histplot(df[col], kde=True, ax=axes[idx], color='skyblue')
            axes[idx].set_title(f'Distribution: {col}', fontweight='bold')
            axes[idx].set_xlabel(col)
            axes[idx].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig('outputs/feature_distributions.png', dpi=300, bbox_inches='tight')
    print("Saved: outputs/feature_distributions.png")
    plt.close()
    
    # Visualization 3: Scatter Plots (Features vs Target)
    features = ['ac_hours_per_day', 'num_appliances', 'room_area', 
                'ac_temperature', 'num_people']
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for idx, feature in enumerate(features):
        axes[idx].scatter(df[feature], df['electricity_bill'], 
                         alpha=0.6, edgecolors='k')
        axes[idx].set_xlabel(feature, fontweight='bold')
        axes[idx].set_ylabel('Electricity Bill', fontweight='bold')
        axes[idx].set_title(f'{feature} vs Bill')
        
        # Add regression line
        z = np.polyfit(df[feature], df['electricity_bill'], 1)
        p = np.poly1d(z)
        axes[idx].plot(df[feature], p(df[feature]), "r--", alpha=0.8)
    
    # Remove extra subplot
    fig.delaxes(axes[5])
    
    plt.tight_layout()
    plt.savefig('outputs/scatter_plots.png', dpi=300, bbox_inches='tight')
    print("Saved: outputs/scatter_plots.png")
    plt.close()
    
    # Visualization 4: Box Plots (Outlier Detection)
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for idx, col in enumerate(df.columns):
        if idx < len(axes):
            sns.boxplot(y=df[col], ax=axes[idx], color='lightgreen')
            axes[idx].set_title(f'Box Plot: {col}', fontweight='bold')
            axes[idx].set_ylabel(col)
    
    plt.tight_layout()
    plt.savefig('outputs/boxplots_outliers.png', dpi=300, bbox_inches='tight')
    print("Saved: outputs/boxplots_outliers.png")
    plt.close()
    
    # Visualization 5: Interactive Plotly 3D Scatter
    fig = px.scatter_3d(df, 
                        x='ac_hours_per_day', 
                        y='room_area', 
                        z='electricity_bill',
                        color='num_appliances',
                        size='num_people',
                        title='3D Visualization: AC Hours vs Room Area vs Bill')
    
    fig.update_layout(height=600)
    fig.write_html('outputs/interactive_3d_plot.html')
    print("Saved: outputs/interactive_3d_plot.html")
    
    # 5. Key Insights
    print("\n5. KEY INSIGHTS")
    print("-" * 70)
    
    # Most correlated feature
    most_corr_feature = correlation['electricity_bill'].drop('electricity_bill').abs().idxmax()
    most_corr_value = correlation.loc[most_corr_feature, 'electricity_bill']
    insight1 = f"Most correlated feature: {most_corr_feature} (r={most_corr_value:.3f})"
    print(f"- {insight1}")
    insights.append(insight1)
    
    # Average bill
    avg_bill = df['electricity_bill'].mean()
    median_bill = df['electricity_bill'].median()
    insight2 = f"Average bill: {avg_bill:.2f}, Median bill: {median_bill:.2f}"
    print(f"- {insight2}")
    insights.append(insight2)
    
    # AC usage patterns
    avg_ac_hours = df['ac_hours_per_day'].mean()
    insight3 = f"Average AC usage: {avg_ac_hours:.2f} hours/day"
    print(f"- {insight3}")
    insights.append(insight3)
    
    # Room characteristics
    avg_area = df['room_area'].mean()
    insight4 = f"Average room size: {avg_area:.2f} sq.m."
    print(f"- {insight4}")
    insights.append(insight4)
    
    # Save insights to file
    with open('outputs/eda_insights.txt', 'w') as f:
        f.write("\n".join(insights))
        
    print("\n" + "=" * 70)
    print("EDA COMPLETE - Check outputs/ folder for visualizations")
    print("=" * 70)

if __name__ == "__main__":
    run_eda()
