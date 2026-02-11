# Phase 3 Walkthrough: Web Application

## Overview
This phase focused on building the interactive web application using Streamlit and preparing it for deployment.

## Step-by-Step Guide

### 1. Streamlit Application
```bash
streamlit run app.py
```
**Features Implemented:**
- **Dynamic Inputs:** Sliders for AC usage (0-24 hrs), Area (10-100 sqm), Temperature (18-30°C).
- **Responsive Layout:** 2-column layout (Inputs | Results).
- **Visual Feedback:** Gauge chart updates instantly.
- **Sample Scenarios:** Pre-defined buttons to quickly populate inputs and see bill estimates.

### 2. Deployment Configuration
Files created for cloud hosting:
- `requirements.txt`: Lists all Python libraries (sklearn, pandas, streamlit).
- `Procfile`: Command for Heroku/Streamlit Cloud (`web: streamlit run app.py`).
- `runtime.txt`: Specifies Python version (`python-3.9.12`).

### 3. Model Loading
- The app loads `models/model_optimized.pkl` and `models/scaler.pkl` on startup.
- These files were force-added to git (`git add -f`) to ensure they are available in the repository for deployment.

## Key Findings
- Streamlit's `st.cache_resource` is used to load the model only once, improving app performance.
- The `plotly` gauge chart provides a much better user experience than a simple text output.

## Files Overview
```
root/
├── app.py                  # Main application code
├── requirements.txt        # Dependencies
├── Procfile                # Deployment command
├── runtime.txt             # Python version
|
└── .streamlit/
    └── config.toml         # Theme settings (Pink/White)
```

## Next Phase
Ready for final documentation in Phase 5.
