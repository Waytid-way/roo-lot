"""
Roo-Lot Chatbot - Result Card Component

IMPORTANT: Display ONLY what the model actually predicts (Report Chapter 4.2)
- Model outputs: Total energy_consumption_kwh (float)
- Model does NOT output: AC vs Appliances breakdown
- Model metrics: R² = 0.9851, MAE = 16.95 kWh, RMSE = 21.67 kWh

Last Updated: 2026-02-13 21:40 ICT (Updated metrics to match retrained model)
"""

import streamlit as st
import plotly.graph_objects as go

def render_result_card(prediction_data: dict, expanded: bool = False):
    """
    Render prediction result card - HONEST OUTPUT ONLY
    
    Args:
        prediction_data: Dictionary with prediction results
        expanded: Whether to show detailed view
    """
    
    amount = prediction_data['amount']
    kwh = prediction_data.get('kwh', amount)
    
    # Get MODEL metrics from Report Chapter 4.2 (Retrained Model 2026-02-13)
    MODEL_R2 = 0.9851       # 98.51% accuracy
    MODEL_MAE_KWH = 16.95   # Mean Absolute Error in kWh
    MODEL_RMSE_KWH = 21.67  # Root Mean Squared Error in kWh
    PRICE_PER_KWH = 4.2     # Approximate THB/unit
    
    # Calculate error in THB
    mae_thb = MODEL_MAE_KWH * PRICE_PER_KWH    # ≈ 71 THB
    rmse_thb = MODEL_RMSE_KWH * PRICE_PER_KWH  # ≈ 91 THB
    
    # CSS Styles
    st.markdown("""
    <style>
    .result-card {
        background-color: var(--color-bg-surface);
        border: 1px solid var(--color-border);
        border-radius: 16px;
        padding: 24px;
        margin: 24px 0;
        transition: all var(--transition-base);
    }
    
    .result-card:hover {
        border-color: var(--color-border-hover);
        transform: translateY(-2px);
    }
    
    .result-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 20px;
    }
    
    .result-icon {
        font-size: 20px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .result-label {
        font-family: var(--font-mono);
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.1em;
        color: var(--color-text-muted);
    }
    
    .result-amount {
        display: flex;
        align-items: baseline;
        gap: 8px;
        margin-bottom: 8px;
    }
    
    .amount-value {
        font-family: var(--font-mono);
        font-size: 56px;
        font-weight: 700;
        background: linear-gradient(135deg, var(--color-accent-blue) 0%, var(--color-accent-green) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
    }
    
    .amount-unit {
        font-family: var(--font-mono);
        font-size: 20px;
        font-weight: 600;
        color: var(--color-text-secondary);
    }
    
    .result-subtitle {
        font-size: 14px;
        color: var(--color-text-secondary);
        margin-bottom: 24px;
        font-family: var(--font-mono);
    }
    
    .result-stats-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        margin-bottom: 20px;
        padding-top: 20px;
        border-top: 1px solid var(--color-border);
    }
    
    .stat-cell {
        text-align: center;
    }
    
    .stat-value {
        font-family: var(--font-mono);
        font-size: 18px;
        font-weight: 600;
        color: var(--color-text-primary);
        margin-bottom: 4px;
    }
    
    .stat-label {
        font-size: 11px;
        color: var(--color-text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    @media (max-width: 768px) {
        .amount-value {
            font-size: 40px;
        }
        
        .result-stats-grid {
            grid-template-columns: 1fr;
            gap: 12px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Main Result Card - NO FABRICATED BREAKDOWN
    st.markdown(f"""<div class="result-card scale-in">
<div class="result-header">
<div class="result-icon">⚡</div>
<div class="result-label">ELECTRICITY BILL PREDICTION</div>
</div>
<div class="result-amount">
<span class="amount-value">{amount:.2f}</span>
<span class="amount-unit">THB</span>
</div>
<div class="result-subtitle">
{kwh:.2f} kWh × {PRICE_PER_KWH} THB/unit
</div>
<div class="result-stats-grid">
<div class="stat-cell">
<div class="stat-value">{MODEL_R2*100:.1f}%</div>
<div class="stat-label">R² Score</div>
</div>
<div class="stat-cell">
<div class="stat-value">±{mae_thb:.2f}฿</div>
<div class="stat-label">Typical Error</div>
</div>
</div>
</div>""", unsafe_allow_html=True)
    
    # Disclaimer - Transparency!
    st.markdown("""
<div style="color: #e0e0e0; font-size: 0.9em; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 5px;">
⚠️ <strong>หมายเหตุสำคัญ</strong>:<br>
• นี่คือค่าการใช้ไฟรวมทั้งหมด ไม่ได้แยกตามเครื่องใช้<br>
• Model ทำนายเป็นค่าเฉลี่ยตลอดปี (อาจต่างจริง ±20% ในเดือนร้อน/หนาว)<br>
• ควรเผื่อค่าใช้จ่าย เพื่อความปลอดภัย
</div>
""", unsafe_allow_html=True)
    
    # Detailed Analysis (optional expand)
    with st.expander("📊 ดูรายละเอียดเพิ่มเติม", expanded=expanded):
        render_detailed_analysis(prediction_data, MODEL_R2, MODEL_MAE_KWH, MODEL_RMSE_KWH, mae_thb, rmse_thb)

def render_detailed_analysis(prediction_data: dict, r2: float, mae_kwh: float, rmse_kwh: float, mae_thb: float, rmse_thb: float):
    """Render detailed analysis - HONEST metrics only"""
    
    # Fix metric label colors for dark theme
    st.markdown("""
    <style>
    [data-testid="stMetricLabel"] {
        color: #e0e0e0 !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 รายละเอียดการวิเคราะห์")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "R² Score",
            f"{r2*100:.2f}%",
            help="Model Accuracy - โมเดลอธิบายความแปรปรวนของข้อมูลได้ 98.51%"
        )
    
    with col2:
        st.metric(
            "MAE",
            f"{mae_thb:.0f}฿",
            help=f"Mean Absolute Error - ความคลาดเคลื่อนเฉลี่ย {mae_kwh:.2f} kWh ≈ {mae_thb:.0f} บาท"
        )
    
    with col3:
        st.metric(
            "RMSE",
            f"{rmse_thb:.0f}฿",
            help=f"Root Mean Squared Error - {rmse_kwh:.2f} kWh ≈ {rmse_thb:.0f} บาท"
        )
    
    # Prediction interval
    amount = prediction_data['amount']
    st.info(f"""
🎯 **ช่วงค่าที่เป็นไปได้**: 
{amount - mae_thb:.0f} - {amount + mae_thb:.0f} ฿

💡 ค่าจริงมักอยู่ในช่วง ±{mae_thb:.0f} บาท จากค่าที่ทำนาย
""")
    
    # System Limitations Disclosure
    st.markdown("---")
    st.markdown("### ⚠️ ข้อจำกัดของระบบ (กรุณาอ่าน)")
    st.markdown("""
### ข้อจำกัดทางเทคนิค

1. **ข้อมูลจำลองฤดูกาล**: 
   - Model เทรนด้วยข้อมูลที่มี synthetic date distribution
   - ค่าทำนายเป็นค่าเฉลี่ยตลอดปี ไม่สะท้อนความแตกต่างตามฤดูกาลจริง
   - **ผลกระทบ**: อาจต่ำกว่าจริง ~15% ในเดือนร้อน (เมษา-มิถุนา)
     และสูงกว่าจริง ~30% ในเดือนหนาว (พฤศจิกา-กุมภา)

2. **ขอบเขตข้อมูล**:
   - Model เทรนด้วยข้อมูลบ้าน 1-6 คน (ส่วนใหญ่ 2-4 คน)
   - บ้านที่มีสมาชิก > 6 คน อาจได้ค่าทำนายที่คลาดเคลื่อนสูง

3. **ไม่รองรับรายละเอียดเครื่องใช้**:
   - Model ไม่ทราบประเภท/จำนวนเครื่องใช้ไฟฟ้าแต่ละชนิด
   - พยากรณ์จากจำนวนคนและการมีแอร์เท่านั้น

4. **พฤติกรรมต่างประเทศ**:
   - ข้อมูลเทรนมาจาก international dataset
   - อาจแตกต่างจากพฤติกรรมการใช้ไฟของคนไทย

### แนวทางใช้งาน
✅ ใช้เป็น **แนวทางประมาณการ** ไม่ใช่ค่าแน่นอน  
✅ เหมาะสำหรับการวางแผนงบประมาณเบื้องต้น  
✅ ควรเผื่อค่าใช้จ่าย ±20% เพื่อความปลอดภัย
""")
