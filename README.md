# Roo-Lot: Electricity Bill Prediction System

## 🎯 Project Overview
Roo-Lot is a machine learning-powered web application designed to help dormitory residents and homeowners estimate their monthly electricity bills. By inputting usage details including room size, AC usage, and appliance counts, the system provides accurate predictions to aid in financial planning. This project utilizes a Random Forest Regression model trained on household energy consumption data to deliver precise estimates.

## 🚀 Quick Start

### Installation
```bash
# Python 3.9+ required
pip install -r requirements.txt
```

### Training
```bash
python scripts/train_model.py
# Expected output (on full dataset): R² = 0.93, MAE = 1.13 kWh
# Training time: ~2 minutes
```

### Running Web App
```bash
streamlit run app_chatbot.py
# Opens at http://localhost:8501
```

## 📊 Performance Metrics

| Model | R² | MAE (kWh) | RMSE (kWh) | Training Time |
|-------|-----|-----------|------------|---------------|
| **Random Forest** | **0.9851** | **16.95** | **21.67** | 120s |
| Linear Regression | 0.9145 | 1.27 | 1.61 | 5s |

## 🏗️ Project Structure

```
roo-lot/
├── scripts/
│   └── train_model.py      # Model training pipeline
├── utils/
│   └── model_predictor.py  # Inference engine
├── app_chatbot.py          # Streamlit UI
├── outputs/
│   ├── eda/                # EDA visualizations
│   └── model_viz/          # Model performance plots
├── models/
│   └── electricbills_predict.pkl # Trained Random Forest model
└── data/
    └── household_energy.csv # Dataset
```

## 🔬 Technical Details

### Feature Engineering
- **Seasonal features**: Hot (Mar-Jun), Rainy (Jul-Oct), Cool (Nov-Feb)
- **Weekend ratio**: Proportion of Sat-Sun in month
- **Household size**: 1-10 people (primary predictor - 86% importance)

### Model Configuration
```python
RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_split=2,
    random_state=42
)
```

## ⚠️ Known Limitations
- **Synthetic Date Distribution**: The model training uses synthetic dates to demonstrate seasonal feature engineering, which may not perfectly reflect real-world seasonality (see Report Section 5.2).
- **Domain Specificity**: Trained on international data; patterns may differ slightly for Thai households.
- **Extrapolation**: Predictions for household sizes > 10 may be less accurate.

## 📚 Documentation
- **Full Report**: [Report ML Project (Roo-Lot).md](./Report%20ML%20Project%20(Roo-Lot).md)
- **Kaggle Dataset**: [Link](https://www.kaggle.com/datasets/samxsam/household-energy-consumption)

## 🤝 Contributing
Contributions are welcome! Please submit a Pull Request.

## 📄 License
MIT License
