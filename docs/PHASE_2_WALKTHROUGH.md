# Phase 2 Walkthrough: Model Development

## Overview
This phase covers the development, training, evaluation, and selection of the regression model.

## Step-by-Step Guide

### 1. Model Training
```bash
python scripts/train_model.py
```
**Output:** Trained Linear Regression model with 5-fold cross-validation.
- Train R2: 0.9923
- Test R2: 0.9923
- Model saved to `models/model.pkl`

### 2. Model Evaluation
```bash
python scripts/evaluate_model.py
```
**Output:** Comprehensive report with metrics and plots.
- MAE: 43.67 Baht
- Evaluation report saved to `outputs/evaluation_report.txt`
- Plot saved to `outputs/model_evaluation.png`

### 3. Hyperparameter Tuning
```bash
python scripts/optimize_model.py
```
**Output:** Grid Search performed on 5 algorithms (Linear, Ridge, Lasso, ElasticNet, RandomForest).
- **Best Model:** Lasso Regression
- **Best Params:** `{'alpha': 0.1}`
- Optimized model saved to `models/model_optimized.pkl`

## Key Findings
- **Lasso Regression** performed best due to its ability to handle slight collinearity and perform implicit feature selection.
- All linear models (Linear, Ridge, Lasso) performed significantly better than RandomForest (0.99 vs 0.97 R2), confirming the linear nature of the data.
- The model is highly accurate with <3% mean absolute percentage error (MAPE).

## Files Overview
```
models/
├── model.pkl               # Initial trained model
├── model_optimized.pkl     # Final optimized model (Lasso)
├── scaler.pkl              # Feature scaler for use in app
└── model_metadata.json     # Training metadata

scripts/
├── train_model.py          # Training pipeline
├── evaluate_model.py       # Evaluation logic
└── optimize_model.py       # Hyperparameter tuning

outputs/
├── model_evaluation.png    # Residual analysis
├── evaluation_report.txt   # Detailed metrics
├── model_comparison.png    # Bar chart of models
└── model_comparison.csv    # Results table

docs/
└── MODEL_SELECTION.md      # Final recommendation
```

## Next Phase
Ready for Phase 3: Building the Streamlit Web Application.
