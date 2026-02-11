# Phase 1 Walkthrough: Data Management

## Overview
This phase covers data collection, preprocessing, and exploratory analysis.

## Step-by-Step Guide

### 1. Data Collection
```bash
python scripts/validate_data.py
```
**Output:** Validation report showing 100 clean samples.
(Errors about outliers are expected during validation as the raw data hasn't been cleaned yet).

### 2. Data Preprocessing
```bash
python scripts/preprocess_data.py
```
**Output:** Cleaned data with outliers removed, features scaled.
Original: 100 samples -> Cleaned: 89 samples.

### 3. Exploratory Data Analysis
```bash
python scripts/eda.py
```
**Output:** 5 visualizations saved in `outputs/`

## Key Findings
- AC usage is the primary driver of electricity costs (r=0.974).
- Room area also contributes but less significantly.
- AC temperature has a negative correlation (as expected, lower temp = higher bill).
- 11 outliers detected and removed from the synthetic dataset.

## Files Overview
```
data/
├── electricity_data_template.csv    # Template for user data entry
├── electricity_data_sample.csv      # 100 synthetic samples
├── electricity_data_processed.csv   # Cleaned and scaled data
└── preprocessing_report.txt         # Preprocessing statistics

scripts/
├── validate_data.py                 # Validation functions
├── preprocess_data.py               # Preprocessing pipeline
└── eda.py                           # EDA script

outputs/
├── correlation_heatmap.png
├── feature_distributions.png
├── scatter_plots.png
├── boxplots_outliers.png
├── interactive_3d_plot.html
└── eda_insights.txt
```

## Next Phase
Ready for model training in Phase 2.
