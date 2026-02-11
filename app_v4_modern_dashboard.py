"""
Roo-Lot: Modern Electricity Bill Predictor
Version: 4.0.0 - React-Inspired Multi-Theme Dashboard

A machine learning powered web application with modern multi-theme UI
Ported from React design system to Streamlit
Themes: Dark, Muji, Minimal

Author: Roo-Lot Dev Team
Date: February 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import datetime
import time
import os
from typing import Optional, Dict, Any

# Import custom modules
from utils.theme_system import generate_css, get_theme_colors, get_theme_info, get_available_themes
from utils.charts import create_modern_gauge, create_simple_arc_gauge, create_status_indicator

# ===== Page Configuration =====
st.set_page_config(
    page_title="รู้หลอด | Electricity Bill Predictor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== Constants =====
MAX_REASONABLE_BILL = 50000
MAX_UNIT_INPUT = 2000
MAX_USAGE_CHANGE_PCT = 3.0

# ===== Translations =====
TRANSLATIONS = {
    'en': {
        'appTitle': "Roo-Lot",
        'role': "System Operator",
        'menu': "Main Menu",
        'dashboard': "Dashboard",
        'prediction': "Prediction",
        'history': "History",
        'config': "Configuration",
        
        'headerTitle': "Electricity Bill Predictor",
        'headerDesc': "Predict next month's electricity bill with Machine Learning.",
        
        'paramsTitle': "Model Parameters",
        'paramsDesc': "Configure inputs for the prediction engine.",
        'date': "Date",
        'time': "Time",
        'factors': "External Factors",
        'schoolBreak': "School Break",
        'schoolBreakDesc': "Is it currently a school holiday?",
        'specialEvent': "Special Event",
        'specialEventDesc': "High traffic expected event nearby",
        
        'btnPredict': "Run Prediction",
        'btnProcessing': "Processing...",
        
        'resultTitle': "Prediction Result",
        'unit': "Units",
        'baht': "THB",
        'waiting': "Waiting for input parameters...",
        'updated': "Last updated just now",
        'confidence': "Confidence",
        
        'histTitle': "Prediction History",
        'histDesc': "Recent model executions and results.",
        'export': "Export CSV",
        'colTime': "Timestamp",
        'colBreak': "Break",
        'colPred': "Prediction",
        'colStatus': "Status",
        
        'statusNormal': "Normal",
        'statusHigh': "High",
        'statusLow': "Low",
        
        'toastSuccess': "Prediction Successful",
        'toastDesc': "Model has updated the results.",
        
        'lang': "Language",
        'theme': "Theme",
        'selectTheme': "Select Theme",
        
        # Input fields
        'current_unit': 'Current Month Units (kWh)',
        'previous_unit': 'Previous Month Units (kWh)',
        'people_count': 'Number of People',
        'target_month': 'Target Month',
        'is_break': 'School Break',
        
        'calculating': 'Calculating...',
        'trySample': 'Try Sample Data',
        
        'usageCategory': 'Usage Category',
        'lowUsage': 'Low (Efficient)',
        'moderateUsage': 'Moderate',
        'highUsage': 'High (Heavy)',
    },
    'th': {
        'appTitle': "รู้หลอด",
        'role': "ผู้ดูแลระบบ",
        'menu': "เมนูหลัก",
        'dashboard': "แดชบอร์ด",
        'prediction': "ทำนายค่าไฟ",
        'history': "ประวัติ",
        'config': "ตั้งค่า",
        
        'headerTitle': "ทำนายค่าไฟฟ้า",
        'headerDesc': "ทำนายค่าไฟเดือนหน้าด้วย Machine Learning",
        
        'paramsTitle': "พารามิเตอร์โมเดล",
        'paramsDesc': "กำหนดค่าสำหรับการประมวลผล",
        'date': "วันที่",
        'time': "เวลา",
        'factors': "ปัจจัยภายนอก",
        'schoolBreak': "ปิดเทอม",
        'schoolBreakDesc': "อยู่ในช่วงปิดภาคเรียนหรือไม่?",
        'specialEvent': "กิจกรรมพิเศษ",
        'specialEventDesc': "มีกิจกรรมที่คนพลุกพล่าน",
        
        'btnPredict': "เริ่มการทำนาย",
        'btnProcessing': "กำลังประมวลผล...",
        
        'resultTitle': "ผลลัพธ์การทำนาย",
        'unit': "หน่วย",
        'baht': "บาท",
        'waiting': "รอการป้อนข้อมูล...",
        'updated': "อัปเดตล่าสุดเมื่อสักครู่",
        'confidence': "ความน่าจะเป็น",
        
        'histTitle': "ประวัติการทำนาย",
        'histDesc': "ผลลัพธ์การใช้งานล่าสุด",
        'export': "ส่งออก CSV",
        'colTime': "เวลา",
        'colBreak': "ปิดเทอม",
        'colPred': "ผลทำนาย",
        'colStatus': "สถานะ",
        
        'statusNormal': "ปกติ",
        'statusHigh': "สูง",
        'statusLow': "ต่ำ",
        
        'toastSuccess': "ทำนายสำเร็จ",
        'toastDesc': "โมเดลได้อัปเดตผลลัพธ์แล้ว",
        
        'lang': "ภาษา",
        'theme': "ธีม",
        'selectTheme': "เลือกธีม",
        
        # Input fields
        'current_unit': 'หน่วยไฟเดือนปัจจุบัน (kWh)',
        'previous_unit': 'หน่วยไฟเดือนที่แล้ว (kWh)',
        'people_count': 'จำนวนคน',
        'target_month': 'เดือนที่ต้องการทำนาย',
        'is_break': 'ช่วงปิดเทอม',
        
        'calculating': 'กำลังคำนวณ...',
        'trySample': 'ลองข้อมูลตัวอย่าง',
        
        'usageCategory': 'ระดับการใช้ไฟ',
        'lowUsage': 'ต่ำ (ประหยัด)',
        'moderateUsage': 'ปานกลาง',
        'highUsage': 'สูง (ใช้มาก)',
    }
}

# ===== Custom Exception =====
class PredictionError(Exception):
    """Custom exception for prediction errors"""
    pass


# ===== Model Loading =====
@st.cache_resource
def load_model() -> Optional[Any]:
    """Load the trained prediction model with error handling"""
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'model_v2_next_month.pkl')
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None


# ===== Validation =====
def validate_unit_input(current: int, previous: int) -> tuple[bool, str]:
    """Validate electricity unit inputs"""
    if current < 0 or current > MAX_UNIT_INPUT:
        return False, f"Current unit should be between 0-{MAX_UNIT_INPUT} kWh"
    
    if previous < 0 or previous > MAX_UNIT_INPUT:
        return False, f"Previous unit should be between 0-{MAX_UNIT_INPUT} kWh"
    
    if previous > 0:
        change_pct = abs(current - previous) / previous
        if change_pct > MAX_USAGE_CHANGE_PCT:
            return False, f"Unusual change detected ({change_pct*100:.0f}%). Please verify."
    
    return True, "Valid"


def predict_with_error_handling(model: Any, input_data: pd.DataFrame) -> float:
    """Make prediction with comprehensive error handling"""
    try:
        prediction = model.predict(input_data)[0]
        
        if np.isnan(prediction) or np.isinf(prediction):
            raise PredictionError("Model returned invalid numerical value")
        
        if prediction < 0:
            raise PredictionError("Model predicted negative bill")
        
        if prediction > MAX_REASONABLE_BILL:
            raise PredictionError(f"Unreasonably high bill predicted (>{MAX_REASONABLE_BILL} THB)")
        
        return max(0, prediction)
        
    except PredictionError:
        raise
    except Exception as e:
        raise PredictionError(f"Unexpected prediction error: {str(e)}")


# ===== UI Components =====
def render_sidebar(T: dict, current_theme: str):
    """Render the sidebar navigation"""
    
    with st.sidebar:
        # Logo
        st.markdown(f"""
        <div class="logo-container">
            <div class="logo-icon">⚡</div>
            <div class="logo-text">{T['appTitle']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation Menu
        st.markdown(f'<div class="nav-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="nav-title">{T["menu"]}</div>', unsafe_allow_html=True)
        
        menu_items = [
            ('📊', T['dashboard'], False),
            ('⚡', T['prediction'], True),  # Active
            ('📝', T['history'], False),
            ('⚙️', T['config'], False),
        ]
        
        for icon, label, active in menu_items:
            active_class = 'active' if active else ''
            st.markdown(f'''
            <div class="nav-item {active_class}">
                <span class="nav-icon">{icon}</span>
                <span>{label}</span>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Theme Selector
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div class="nav-title">{T["theme"]}</div>', unsafe_allow_html=True)
        
        themes = get_available_themes()
        theme_cols = st.columns(len(themes))
        
        for idx, theme_name in enumerate(themes):
            theme_info = get_theme_info(theme_name)
            with theme_cols[idx]:
                if st.button(
                    theme_info['icon'],
                    key=f"theme_{theme_name}",
                    use_container_width=True,
                    help=theme_info['name'],
                    type="primary" if current_theme == theme_name else "secondary"
                ):
                    st.session_state.theme = theme_name
                    st.rerun()
        
        # Language Toggle
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div class="nav-title">{T["lang"]}</div>', unsafe_allow_html=True)
        
        lang_col1, lang_col2 = st.columns(2)
        with lang_col1:
            if st.button("🇹🇭 ไทย", use_container_width=True, 
                        type="primary" if st.session_state.language == 'th' else "secondary"):
                st.session_state.language = 'th'
                st.rerun()
        with lang_col2:
            if st.button("🇺🇸 EN", use_container_width=True,
                        type="primary" if st.session_state.language == 'en' else "secondary"):
                st.session_state.language = 'en'
                st.rerun()
        
        # User Profile
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="padding: 12px; background: var(--bg-input); border-radius: 12px; border: 1px solid var(--border-default);">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; display: flex; align-items: center; justify-center; color: white; font-weight: 600; font-size: 14px;">
                    AD
                </div>
                <div>
                    <div style="color: var(--text-heading); font-size: 14px; font-weight: 500;">Admin User</div>
                    <div style="color: var(--text-muted); font-size: 12px;">{T['role']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_input_form(T: dict, model: Any):
    """Render the input form card (Left Column)"""
    
    st.markdown(f"""
    <div class="card-header">
        <span class="card-icon">⚙️</span>
        <div>
            <div class="card-title">{T['paramsTitle']}</div>
            <div class="card-description">{T['paramsDesc']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Wrap in form for batch updates
    with st.form("prediction_form"):
        # Time inputs in a styled container
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input(
                T['date'],
                value=datetime.date.today(),
                label_visibility="visible"
            )
        with col2:
            time_val = st.time_input(
                T['time'],
                value=datetime.time(8, 30),
                label_visibility="visible"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Main parameters
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            current_unit = st.number_input(
                T['current_unit'],
                min_value=0,
                max_value=MAX_UNIT_INPUT,
                value=150,
                step=10
            )
        with col2:
            lag1_unit = st.number_input(
                T['previous_unit'],
                min_value=0,
                max_value=MAX_UNIT_INPUT,
                value=140,
                step=10
            )
        
        col1, col2 = st.columns(2)
        with col1:
            people = st.number_input(
                T['people_count'],
                min_value=1,
                max_value=10,
                value=2
            )
        with col2:
            # Month selection - next 3 months only
            current_month = datetime.datetime.now().month
            month_options = []
            for i in range(3):
                next_month = (current_month + i) % 12
                if next_month == 0:
                    next_month = 12
                month_options.append(next_month)
            
            month = st.selectbox(
                T['target_month'],
                options=month_options,
                index=0,
                format_func=lambda x: datetime.date(2024, x, 1).strftime('%B')
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # External Factors
        st.markdown(f'<div class="input-container">', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; margin-bottom: 12px;">{T["factors"]}</p>', unsafe_allow_html=True)
        
        is_break = st.checkbox(
            f"{T['schoolBreak']} • {T['schoolBreakDesc']}",
            value=False
        )
        
        special_event = st.checkbox(
            f"{T['specialEvent']} • {T['specialEventDesc']}",
            value=False
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit Button
        predict_clicked = st.form_submit_button(
            T['btnPredict'],
            type="primary",
            use_container_width=True
        )
    
    return {
        'current_unit': current_unit,
        'lag1_unit': lag1_unit,
        'people': people,
        'month': month,
        'is_break': 1 if is_break else 0,
        'special_event': special_event,
        'date': date,
        'time': time_val
    }, predict_clicked


def render_result_card(T: dict, theme_colors: dict, prediction: Optional[float], inputs: Optional[dict], lang: str):
    """Render the prediction result card with gauge"""
    
    st.markdown(f"""
    <div class="card-header">
        <span class="card-icon">📊</span>
        <div>
            <div class="card-title">{T['resultTitle']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if prediction is not None and inputs is not None:
        # Display value and gauge
        st.markdown(f"""
        <div class="result-container">
            <div class="result-value">{prediction:.0f}</div>
            <div class="result-unit">{T['unit']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Gauge Chart
        fig = create_modern_gauge(prediction, theme_colors, lang=lang, unit=T['unit'])
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
       # Status and Confidence
        status_text, status_class = create_status_indicator(prediction, lang)
        
        st.markdown(f"""
        <div style="text-align: center; margin-top: 20px;">
            <div class="status-badge {status_class}">
                {T['usageCategory']}: {status_text}
            </div>
            <div class="confidence-indicator" style="margin-top: 16px;">
                <div class="confidence-dot"></div>
                <span>{T['confidence']}: 94.2% • {T['updated']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        # Empty state
        st.markdown(f"""
        <div class="empty-state">
            <div class="empty-state-icon">⚡</div>
            <div class="empty-state-text">{T['waiting']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample data button
        if st.button(f"📝 {T['trySample']}", use_container_width=True):
            st.session_state.prediction = 1248.50
            st.session_state.prediction_inputs = {
                'current_unit': 250,
                'lag1_unit': 240,
                'people': 3,
                'month': (datetime.datetime.now().month % 12) + 1,
                'is_break': 0
            }
            st.rerun()


def render_history_table(T: dict):
    """Render the history table"""
    
    st.markdown(f"""
    <div class="card-header">
        <span class="card-icon">📝</span>
        <div>
            <div class="card-title">{T['histTitle']}</div>
            <div class="card-description">{T['histDesc']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mock history data
    history_data = [
        {'timestamp': '2026-02-12 08:00', 'schoolBreak': 'No', 'prediction': 845.5, 'status': 'Normal'},
        {'timestamp': '2026-02-11 17:30', 'schoolBreak': 'No', 'prediction': 1292.1, 'status': 'High'},
        {'timestamp': '2026-02-11 08:00', 'schoolBreak': 'Yes', 'prediction': 450.2, 'status': 'Low'},
    ]
    
    # Custom HTML table
    table_html = f"""
    <table class="history-table">
        <thead>
            <tr>
                <th>{T['colTime']}</th>
                <th style="text-align: center;">{T['colBreak']}</th>
                <th style="text-align: right;">{T['colPred']}</th>
                <th style="text-align: center;">{T['colStatus']}</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for row in history_data:
        status_text = T['statusNormal'] if row['status'] == 'Normal' else (T['statusHigh'] if row['status'] == 'High' else T['statusLow'])
        status_class = 'success' if row['status'] == 'Normal' else ('error' if row['status'] == 'High' else 'info')
        
        table_html += f"""
            <tr>
                <td class="timestamp">{row['timestamp']}</td>
                <td style="text-align: center;">
                    <span class="status-badge {'info' if row['schoolBreak'] == 'Yes' else 'success'}" style="padding: 4px 8px; font-size: 10px;">
                        {row['schoolBreak']}
                    </span>
                </td>
                <td style="text-align: right; font-weight: 500;">{row['prediction']:.2f}</td>
                <td style="text-align: center;">
                    <span class="status-badge {status_class}" style="padding: 4px 12px; font-size: 10px;">
                        {status_text}
                    </span>
                </td>
            </tr>
        """
    
    table_html += """
        </tbody>
    </table>
    """
    
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Export button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(f"📥 {T['export']}", use_container_width=True):
        df = pd.DataFrame(history_data)
        csv = df.to_csv(index=False)
        st.download_button(
            label=T['export'],
            data=csv,
            file_name=f"roolot_history_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )


def show_toast(T: dict):
    """Show success toast notification"""
    st.markdown(f"""
    <div class="toast">
        <div class="toast-icon">✅</div>
        <div class="toast-content">
            <div class="toast-title">{T['toastSuccess']}</div>
            <div class="toast-desc">{T['toastDesc']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ===== Main Application =====
def main():
    """Main application entry point"""
    
    # Initialize session state
    if 'language' not in st.session_state:
        st.session_state.language = 'th'  # Default Thai
    
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'  # Default Dark
    
    if 'prediction' not in st.session_state:
        st.session_state.prediction = None
    
    if 'prediction_inputs' not in st.session_state:
        st.session_state.prediction_inputs = None
    
    if 'show_toast' not in st.session_state:
        st.session_state.show_toast = False
    
    # Get current settings
    lang = st.session_state.language
    theme = st.session_state.theme
    T = TRANSLATIONS[lang]
    theme_colors = get_theme_colors(theme)
    
    # Apply theme CSS
    css = generate_css(theme)
    st.markdown(css, unsafe_allow_html=True)
    
    # Render Sidebar
    render_sidebar(T, theme)
    
    # Load Model
    model = load_model()
    if model is None:
        st.error("⚠️ Model not found. Please train the model first.")
        st.stop()
    
    # Header
    st.markdown(f"""
    <div style="margin-bottom: 32px;">
        <h1 style="color: var(--text-heading); font-size: 32px; font-weight: 700; margin-bottom: 8px;">
            {T['headerTitle']}
        </h1>
        <p style="color: var(--text-muted); font-size: 14px;">
            {T['headerDesc']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Layout: 5/12 + 7/12 columns (React grid)
    col_left, col_right = st.columns([5, 7], gap="large")
    
    # LEFT COLUMN: Input Form
    with col_left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        inputs, predict_clicked = render_input_form(T, model)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # RIGHT COLUMN: Result + History
    with col_right:
        # Result Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        render_result_card(T, theme_colors, st.session_state.prediction, st.session_state.prediction_inputs, lang)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # History Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        render_history_table(T)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle Prediction
    if predict_clicked:
        is_valid, msg = validate_unit_input(inputs['current_unit'], inputs['lag1_unit'])
        
        if not is_valid:
            st.warning(f"⚠️ {msg}")
        
        input_data = pd.DataFrame({
            'current_unit': [inputs['current_unit']],
            'is_break': [inputs['is_break']],
            'month': [inputs['month']],
            'people': [inputs['people']],
            'lag1_unit': [inputs['lag1_unit']]
        })
        
        try:
            with st.spinner(T['calculating']):
                time.sleep(1)  # Simulate processing
                prediction = predict_with_error_handling(model, input_data)
            
            st.session_state.prediction = prediction
            st.session_state.prediction_inputs = inputs
            st.session_state.show_toast = True
            st.success(f"✅ {T['toastSuccess']}")
            st.rerun()
            
        except PredictionError as e:
            st.error(f"❌ Error: {str(e)}")
    
    # Show toast if flag is set
    if st.session_state.show_toast:
        show_toast(T)
        st.session_state.show_toast = False
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: var(--text-muted); font-size: 12px; padding: 20px 0;">
        รู้หลอด v4.0.0 - Modern Multi-Theme Dashboard | Theme: {get_theme_info(theme)['name']} | Language: {lang.upper()}
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
