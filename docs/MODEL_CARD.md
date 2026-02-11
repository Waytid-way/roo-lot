# Model Card: Roo-Lot Electricity Predictor

## Model Details
**Experiment Date:** 2026-02-11
**Model Version:** 1.0.0
**Model Type:** Lasso Regression
**Framework:** Scikit-learn 1.3+
**Language:** Python 3.9+
**License:** MIT

## Intended Use
**Primary Use Case:** Estimating monthly electricity bills for residential units (dormitories/apartments).
**Target Users:** Students, renters, landlords.
**Out of Scope:** Industrial electricity prediction, complex multi-rate tariffs.

## Training Data
**Source:** Synthetic dataset generated based on realistic assumptions of appliance power consumption in Thailand.
**Size:** 100 samples (80 training / 20 testing).
**Features:**
- `ac_hours_per_day` (Float): Hours of air conditioner usage.
- `num_appliances` (Int): Count of electrical appliances.
- `room_area` (Float): Room size in square meters.
- `ac_temperature` (Float): AC temperature setting (Celsius).
- `num_people` (Int): Number of occupants.

## Performance Metrics
Evaluated on a hold-out test set (20% of data):

| Metric | Value |
|--------|-------|
| **R2 Score** | 0.9923 |
| **MAE** | 43.63 Baht |
| **RMSE** | 58.41 Baht |
| **MAPE** | 2.98% |

## Limitations
- **Synthetic Data:** The model is trained on synthetic data which may not perfectly reflect real-world variance (e.g., faulty appliances, vampire power).
- **Linear Assumption:** The model assumes linearity between usage and cost, which is generally true but may miss non-linear pricing step-ups (progressive tariff rates).
- **Location:** The base rate is hardcoded in the data generation logic (approx. 5 Baht/unit implied), which might differ by location.

## Ethical Considerations
- **Privacy:** No personal identifiable information (PII) is used or stored.
- **Fairness:** The model relies purely on usage metrics and does not use demographic data that could bias the cost estimation unfairly.
