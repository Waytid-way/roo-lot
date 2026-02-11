# Real Data V2 Retraining Report

## Model Performance
- **Model:** Ridge Regression
- **Features:** ['current_unit', 'is_break', 'month', 'people', 'lag1_unit']
- **MAE (Test):** 269.69
- **RMSE (Test):** 295.78
- **Intercept:** 595.91

## Feature Coefficients
- **current_unit:** 3.0201
- **is_break:** 88.6071
- **month:** -4.2268
- **people:** 25.2474
- **lag1_unit:** -1.3419

## Test Set Predictions
| Date | Actual | Predicted | Error |
|---|---|---|---|
| 2025-09-01 | 1264.00 | 892.54 | 371.46 |
| 2025-10-01 | 1192.00 | 890.76 | 301.24 |
| 2025-11-01 | 1136.00 | 837.89 | 298.11 |
| 2025-12-01 | 480.00 | 824.60 | -344.60 |
| 2026-01-01 | 704.00 | 670.95 | 33.05 |
