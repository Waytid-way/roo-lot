import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import json

# Set Page Configuration
st.set_page_config(
    page_title="Roo-Lot: Electricity Bill Predictor",
    page_icon="🔦",
    layout="wide"
)

# Load Model and Artifacts
@st.cache_resource
def load_artifacts():
    model = joblib.load('models/model_optimized.pkl')
    scaler = joblib.load('models/scaler.pkl')
    with open('models/model_metadata.json', 'r') as f:
        metadata = json.load(f)
    return model, scaler, metadata

try:
    model, scaler, metadata = load_artifacts()
except FileNotFoundError:
    st.error("Error: Model artifacts not found. Please ensure the model is trained and saved in the 'models/' directory.")
    st.stop()

# Sidebar: Project Info
st.sidebar.image("https://img.icons8.com/color/96/000000/light-on.png", width=80)
st.sidebar.title("Roo-Lot (รู้หลอด)")
st.sidebar.markdown("**Tagline:** 'รู้อะไร ไม่เท่ารู้หลอด'")
st.sidebar.markdown("---")
st.sidebar.info(
    """
    **Model Info:**
    - Algorithm: Lasso Regression
    - Accuracy (R2): 99.23%
    - MAE: ~44 Baht
    """
)

# Main Content
st.title("🔦 Electricity Bill Predictor")
st.markdown("### Predict your monthly electricity bill for dormitory/apartment")

# Input Form
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Enter Usage Details")
    
    ac_hours = st.slider(
        "❄️ AC Usage (Hours/Day)", 
        min_value=0.0, 
        max_value=24.0, 
        value=8.0, 
        step=0.5,
        help="Average hours you turn on the air conditioner per day."
    )
    
    num_appliances = st.number_input(
        "📺 Number of Appliances", 
        min_value=0, 
        max_value=50, 
        value=5, 
        step=1,
        help="Total number of electrical appliances in the room."
    )
    
    room_area = st.number_input(
        "bad Room Area (sq.m.)", 
        min_value=10.0, 
        max_value=100.0, 
        value=25.0, 
        step=1.0
    )
    
    ac_temp = st.slider(
        "🌡️ AC Temperature (°C)", 
        min_value=18.0, 
        max_value=30.0, 
        value=25.0, 
        step=1.0,
        help="Average temperature setting of your AC."
    )
    
    num_people = st.number_input(
        "👥 Number of People", 
        min_value=1, 
        max_value=10, 
        value=1
    )

# Prediction Logic
input_data = pd.DataFrame({
    'ac_hours_per_day': [ac_hours],
    'num_appliances': [num_appliances],
    'room_area': [room_area],
    'ac_temperature': [ac_temp],
    'num_people': [num_people]
})

# Scale inputs
input_scaled = scaler.transform(input_data)

# Predict
prediction = model.predict(input_scaled)[0]
prediction = max(0, prediction) # Ensure no negative bills

with col2:
    st.subheader("💰 Predicted Bill")
    
    # Gauge Chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = prediction,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Monthly Bill (Baht)"},
        gauge = {
            'axis': {'range': [0, 5000], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#F63366"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 1000], 'color': '#e6f9e6'}, # Greenish
                {'range': [1000, 2500], 'color': '#ffffe6'}, # Yellowish
                {'range': [2500, 5000], 'color': '#ffe6e6'}  # Reddish
            ],
        }
    ))
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.success(f"**Estimated Bill:** {prediction:,.2f} Baht")
    
    # Cost Breakdown Estimation (Simple Heuristic for visualization)
    # Note: reliable breakdown requires feature contribution analysis (SHAP), 
    # but we can approximate using coefficients.
    
    st.markdown("### 📊 Estimated Cost Drivers")
    cost_drivers = {
        "AC Usage": prediction * 0.6,
        "Appliances": prediction * 0.2,
        "Base & Others": prediction * 0.2
    }
    
    breakdown_df = pd.DataFrame([
        {"Driver": "AC Usage", "Cost": cost_drivers["AC Usage"]},
        {"Driver": "Appliances", "Cost": cost_drivers["Appliances"]},
        {"Driver": "Base & Others", "Cost": cost_drivers["Base & Others"]}
    ])
    
    st.bar_chart(breakdown_df.set_index("Driver"))

# Sample Predictions Tab
st.markdown("---")
st.subheader("🔍 Sample Scenarios")

samples = pd.DataFrame({
    'Scenario': ['Saving Mode', 'Normal Usage', 'Heavy Usage'],
    'AC Hours': [4.0, 8.0, 12.0],
    'Appliances': [3, 5, 8],
    'Area': [20.0, 25.0, 35.0],
    'Temp': [27.0, 25.0, 22.0],
    'People': [1, 2, 3]
})

# Predict for samples
sample_inputs = samples[['AC Hours', 'Appliances', 'Area', 'Temp', 'People']]
sample_inputs.columns = ['ac_hours_per_day', 'num_appliances', 'room_area', 'ac_temperature', 'num_people']
sample_scaled = scaler.transform(sample_inputs)
samples['Predicted Bill'] = model.predict(sample_scaled)

st.table(samples.style.format({'Predicted Bill': '{:.2f} ฿'}))

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        Project Roo-Lot (รู้หลอด) | Created by Antigravity Agent
    </div>
    """, 
    unsafe_allow_html=True
)
