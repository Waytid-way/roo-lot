![Roo-Lot Banner](https://img.icons8.com/color/144/000000/light-on.png)

# 💡 Roo-Lot (รู้หลอด)
### "รู้อะไร ไม่เท่ารู้หลอด"
**Predict your monthly electricity bill with Machine Learning**

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Overview
**Roo-Lot** is a machine learning-powered web application designed to help dormitory residents and homeowners estimate their monthly electricity bills. By inputting usage patterns like AC hours, room size, and number of appliances, the app provides an accurate prediction using a trained Lasso Regression model.

The project demonstrates a complete end-to-end ML pipeline:
1. Data Generation & Validation
2. Exploratory Data Analysis (EDA)
3. Model Training & Hyperparameter Tuning
4. Web Application Development
5. Deployment Configuration

## ✨ Key Features
- **Accurate Prediction:** Uses a Lasso Regression model with R2 > 0.99 (on synthetic test data).
- **Interactive UI:** Real-time bill estimation with gauge charts.
- **Scenario Analysis:** Compare costs for different usage patterns (e.g., "Saving Mode" vs. "Heavy Usage").
- **Cost Breakdown:** Visualizes estimated costs from AC, appliances, and base fees.
- **Thai Language Support:** Designed for local users with Thai interface elements.

## 🚀 Installation & Usage

### Prerequisites
- Python 3.8 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/roo-lot.git
cd roo-lot
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```
The app will open in your browser at `http://localhost:8501`.

## 📂 Project Structure
```
roo-lot/
├── app.py                  # Streamlit Web Application
├── data/                   # Dataset files (raw, processed)
├── models/                 # Trained models (.pkl) & metadata
├── notebooks/              # Jupyter notebooks for experiments
├── outputs/                # Evaluation plots & reports
├── scripts/                # Python scripts for ML pipeline
│   ├── validate_data.py    # Data generation
│   ├── preprocess_data.py  # Cleaning & scaling
│   ├── train_model.py      # Model training
│   ├── evaluate_model.py   # Model evaluation
│   └── optimize_model.py   # Hyperparameter tuning
├── docs/                   # Detailed documentation
└── requirements.txt        # Project dependencies
```

## 📊 Model Performance
The best performing model was **Lasso Regression**:
- **Test R2 Score:** 0.9923
- **Mean Absolute Error (MAE):** ~43.63 Baht
- **Root Mean Squared Error (RMSE):** ~58.41 Baht

See full details in [Model Selection Report](docs/MODEL_SELECTION.md).

## 🛠️ Tech Stack
- **Language:** Python
- **ML Framework:** Scikit-learn
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn, Plotly
- **Web Framework:** Streamlit

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

---
*Created by [Your Name] using Antigravity Agent*
