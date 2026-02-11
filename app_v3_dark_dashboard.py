"""
Roo-Lot: Next Month Electricity Bill Predictor
Version: 3.0.0 - Dark Professional Dashboard Edition

A machine learning powered web application with Dark Modern Professional UI
following Invoice Management Dashboard design patterns.
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import datetime
import time
import os
import plotly.graph_objects as go
from typing import Optional, Dict, Any
from contextlib import contextmanager

# ===== Page Configuration =====
st.set_page_config(
    page_title="รู้หลอด | Electricity Bill Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== Dark Theme CSS System =====
DARK_THEME_CSS = """
<style>
/* Import Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Prompt:wght@400;500;600;700&display=swap');

/* CSS Variables */
:root {
    /* Backgrounds */
    --bg-primary: #1A1A1A;
    --bg-secondary: #242424;
    --bg-tertiary: #2D2D2D;
    --bg-elevated: #333333;
    
    /* Text */
    --text-primary: #FFFFFF;
    --text-secondary: #A0A0A0;
    --text-tertiary: #707070;
    
    /* Accent */
    --accent-primary: #F97316;
    --accent-hover: #FB923C;
    --accent-muted: rgba(249, 115, 22, 0.1);
    
    /* Borders */
    --border-subtle: #333333;
    --border-focus: #F97316;
    
    /* Status */
    --success: #10B981;
    --warning: #F59E0B;
    --error: #EF4444;
    --info: #3B82F6;
    
    /* Typography */
    --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-thai: 'Prompt', 'Noto Sans Thai', sans-serif;
}

/* Global Reset */
* {
    font-family: var(--font-primary);
}

/* Main Background */
[data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary) !important;
}

/* Hide default Streamlit elements */
[data-testid="stHeader"] {
    display: none;
}

[data-testid="stToolbar"] {
    display: none;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-subtle);
    min-width: 240px !important;
    max-width: 240px !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 24px 16px !important;
}

/* Sidebar Content */
.sidebar-content {
    color: var(--text-primary);
}

/* Logo Area */
.logo-container {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0 8px 24px 8px;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 24px;
}

.logo-icon {
    width: 40px;
    height: 40px;
    background: var(--accent-primary);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}

.logo-text {
    font-family: var(--font-thai);
    font-size: 20px;
    font-weight: 600;
    color: var(--text-primary);
}

/* Search Bar */
.search-container {
    position: relative;
    margin-bottom: 24px;
}

.search-input {
    width: 100%;
    padding: 10px 14px 10px 36px;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    color: var(--text-primary);
    font-size: 14px;
    outline: none;
    transition: all 0.2s ease;
}

.search-input:focus {
    border-color: var(--border-focus);
    box-shadow: 0 0 0 3px var(--accent-muted);
}

.search-input::placeholder {
    color: var(--text-tertiary);
}

/* Navigation Menu */
.nav-section {
    margin-bottom: 24px;
}

.nav-title {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-tertiary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 0 8px;
    margin-bottom: 8px;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-bottom: 2px;
    font-size: 14px;
    color: var(--text-secondary);
}

.nav-item:hover {
    background: var(--bg-tertiary);
    color: var(--text-primary);
}

.nav-item.active {
    background: var(--bg-tertiary);
    color: var(--text-primary);
    font-weight: 500;
}

.nav-item.active::before {
    content: '';
    position: absolute;
    left: 0;
    width: 3px;
    height: 24px;
    background: var(--accent-primary);
    border-radius: 0 2px 2px 0;
}

.nav-icon {
    font-size: 16px;
    width: 20px;
    text-align: center;
}

/* Main Content Area */
.main-content {
    padding: 24px 32px;
    max-width: calc(100% - 240px - 400px);
}

/* Breadcrumbs */
.breadcrumbs {
    font-size: 13px;
    color: var(--text-tertiary);
    margin-bottom: 8px;
}

.breadcrumbs span {
    color: var(--text-secondary);
}

/* Page Header */
.page-header {
    margin-bottom: 32px;
}

.page-title {
    font-family: var(--font-thai);
    font-size: 28px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 8px 0;
}

.page-subtitle {
    font-family: var(--font-thai);
    font-size: 14px;
    color: var(--text-secondary);
    margin: 0;
}

/* Form Sections */
.form-section {
    background: var(--bg-secondary);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
}

.section-header {
    margin-bottom: 20px;
}

.section-title {
    font-family: var(--font-thai);
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 4px 0;
}

.section-description {
    font-family: var(--font-thai);
    font-size: 13px;
    color: var(--text-secondary);
    margin: 0;
}

/* Input Fields */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div {
    background-color: var(--bg-tertiary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    color: var(--text-primary) !important;
    font-size: 14px !important;
    transition: all 0.2s ease !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stSelectbox > div > div > div:focus {
    border-color: var(--border-focus) !important;
    box-shadow: 0 0 0 3px var(--accent-muted) !important;
}

/* Labels */
.stTextInput label,
.stNumberInput label,
.stSelectbox label {
    font-family: var(--font-thai) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    margin-bottom: 6px !important;
}

/* Toggle Switch */
.stToggle > div {
    background: var(--bg-tertiary) !important;
}

.stToggle > div[data-checked="true"] {
    background: var(--accent-primary) !important;
}

/* Preview Panel */
.preview-panel {
    background: var(--bg-secondary);
    border-left: 1px solid var(--border-subtle);
    min-width: 400px !important;
    max-width: 400px !important;
    height: 100vh;
    position: fixed;
    right: 0;
    top: 0;
    overflow-y: auto;
    padding: 24px;
}

.preview-card {
    background: var(--bg-tertiary);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 32px;
}

.preview-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.preview-title {
    font-family: var(--font-thai);
    font-size: 24px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

/* Buttons */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-primary) !important;
    padding: 10px 20px !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: var(--bg-tertiary) !important;
    border-color: #505050 !important;
}

.stButton > button[kind="primary"] {
    background: var(--accent-primary) !important;
    border: none !important;
    color: #FFFFFF !important;
}

.stButton > button[kind="primary"]:hover {
    background: var(--accent-hover) !important;
}

/* Primary Action Button (Big) */
.predict-btn {
    width: 100%;
    padding: 14px 24px;
    background: var(--accent-primary);
    border: none;
    border-radius: 8px;
    color: #FFFFFF;
    font-family: var(--font-thai);
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-top: 16px;
}

.predict-btn:hover {
    background: var(--accent-hover);
    transform: translateY(-1px);
}

/* Data Table */
.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th {
    text-align: left;
    padding: 12px;
    background: var(--bg-tertiary);
    color: var(--text-secondary);
    font-size: 13px;
    font-weight: 500;
    border-bottom: 1px solid var(--border-subtle);
}

.data-table td {
    padding: 16px 12px;
    border-bottom: 1px solid var(--border-subtle);
    color: var(--text-primary);
    font-size: 14px;
}

.data-table tr:hover td {
    background: var(--bg-tertiary);
}

/* Amount Display */
.amount-display {
    font-size: 48px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 16px 0;
}

.amount-currency {
    font-size: 24px;
    font-weight: 600;
    color: var(--text-secondary);
}

/* Metrics Grid */
.metrics-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 24px;
}

.metric-item {
    padding: 16px;
    background: var(--bg-secondary);
    border-radius: 8px;
    border: 1px solid var(--border-subtle);
}

.metric-label {
    font-size: 12px;
    color: var(--text-secondary);
    margin-bottom: 4px;
}

.metric-value {
    font-size: 20px;
    font-weight: 600;
    color: var(--text-primary);
}

/* Status Badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
}

.status-badge.success {
    background: rgba(16, 185, 129, 0.1);
    color: var(--success);
}

.status-badge.warning {
    background: rgba(245, 158, 11, 0.1);
    color: var(--warning);
}

.status-badge.error {
    background: rgba(239, 68, 68, 0.1);
    color: var(--error);
}

/* User Profile */
.user-profile {
    position: absolute;
    bottom: 24px;
    left: 16px;
    right: 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: var(--bg-tertiary);
    border-radius: 8px;
    border: 1px solid var(--border-subtle);
}

.user-avatar {
    width: 36px;
    height: 36px;
    background: var(--accent-primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    color: #FFFFFF;
}

.user-info {
    flex: 1;
}

.user-name {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
    margin: 0;
}

.user-role {
    font-size: 12px;
    color: var(--text-secondary);
    margin: 0;
}

/* Toast Notification */
[data-testid="stToast"] {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-primary) !important;
}

/* Spinner */
[data-testid="stSpinner"] > div {
    border-color: var(--accent-primary) !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
    background: var(--bg-tertiary);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--bg-elevated);
}

/* Responsive */
@media (max-width: 1200px) {
    .preview-panel {
        display: none;
    }
    
    .main-content {
        max-width: calc(100% - 240px);
    }
}
</style>
"""

# Inject CSS
st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

# ===== Constants =====
MAX_REASONABLE_BILL = 50000  # Max bill for typical household (10k units @ 5 THB/unit)
MAX_UNIT_INPUT = 2000  # Maximum reasonable unit input
MAX_USAGE_CHANGE_PCT = 3.0  # Maximum allowed usage change percentage

# ===== Performance Monitoring =====
@contextmanager
def track_time(operation_name: str):
    """Track and display operation time for debugging"""
    start = time.time()
    yield
    duration = time.time() - start
    if duration > 1.0:
        st.caption(f"Debug: {operation_name} took {duration:.2f}s")


# ===== Model Loading =====
@st.cache_resource
def load_model() -> Optional[Any]:
    """Load the trained prediction model with error handling"""
    try:
        # Use absolute path relative to script location
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'model_v2_next_month.pkl')
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None


# ===== Validation Functions =====
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


class PredictionError(Exception):
    """Custom exception for prediction errors"""
    pass


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


# ===== Translation Dictionary =====
TRANSLATIONS = {
    'th': {
        'dashboard': 'แดชบอร์ด',
        'transactions': 'ธุรกรรม',
        'wallet': 'กระเป๋าเงิน',
        'invoice': 'ใบแจ้งหนี้',
        'budgeting': 'งบประมาณ',
        'reports': 'รายงาน',
        'predict_next_month': 'ทำนายค่าไฟเดือนหน้า',
        'predict_subtitle': 'กรอกข้อมูลการใช้ไฟฟ้าเพื่อทำนายค่าไฟในเดือนถัดไป',
        'usage_details': 'รายละเอียดการใช้ไฟ',
        'usage_details_desc': 'กรอกข้อมูลการใช้ไฟฟ้าของคุณ',
        'current_unit': 'หน่วยไฟเดือนปัจจุบัน (kWh)',
        'previous_unit': 'หน่วยไฟเดือนที่แล้ว (kWh)',
        'people_count': 'จำนวนคน',
        'target_month': 'เดือนที่ต้องการทำนาย',
        'is_break': 'ช่วงปิดเทอม',
        'break_yes': 'ใช่',
        'break_no': 'ไม่ใช่',
        'predict_button': 'ทำนายค่าไฟ',
        'predicted_amount': 'ค่าไฟที่คาดการณ์',
        'baht': 'บาท',
        'usage_category': 'ระดับการใช้ไฟ',
        'low_usage': 'ต่ำ (ประหยัด)',
        'moderate_usage': 'ปานกลาง',
        'high_usage': 'สูง (ใช้มาก)',
        'input_units': 'หน่วยที่กรอก',
        'usage_change': 'เปลี่ยนแปลง',
        'rate_per_unit': 'อัตราต่อหน่วย',
        'download_csv': 'ดาวน์โหลด CSV',
        'preview_result': 'ผลลัพธ์',
        'preview_desc': 'ผลการทำนายค่าไฟฟ้าของคุณ',
        'prediction_date': 'วันที่ทำนาย',
        'confidence': 'ความน่าจะเป็น',
        'note_break': 'หมายเหตุ: ช่วงปิดเทอมอาจส่งผลต่อการใช้ไฟ',
        'validation_warning': 'คำเตือน',
        'error_model_not_found': 'ไม่พบโมเดล',
        'error_model_info': 'กรุณารันคำสั่ง',
        'efficient_user': 'ผู้ใช้ที่ประหยัด',
        'normal_user': 'ผู้ใช้ทั่วไป',
        'heavy_user': 'ผู้ใช้สูง',
        'footer': 'รู้หลอด v3.0.0',
        'search_placeholder': 'ค้นหา...',
        'calculating': 'กำลังคำนวณ...',
        'try_sample': '📝 ลองข้อมูลตัวอย่าง',
    },
    'en': {
        'dashboard': 'Dashboard',
        'transactions': 'Transactions',
        'wallet': 'Wallet',
        'invoice': 'Invoice',
        'budgeting': 'Budgeting',
        'reports': 'Reports',
        'predict_next_month': 'Predict Next Month Bill',
        'predict_subtitle': 'Enter your electricity usage to predict next month\'s bill',
        'usage_details': 'Usage Details',
        'usage_details_desc': 'Enter your electricity consumption data',
        'current_unit': 'Current Month Units (kWh)',
        'previous_unit': 'Previous Month Units (kWh)',
        'people_count': 'Number of People',
        'target_month': 'Target Month',
        'is_break': 'School Break',
        'break_yes': 'Yes',
        'break_no': 'No',
        'predict_button': 'Predict Bill',
        'predicted_amount': 'Predicted Amount',
        'baht': 'THB',
        'usage_category': 'Usage Category',
        'low_usage': 'Low (Efficient)',
        'moderate_usage': 'Moderate',
        'high_usage': 'High (Heavy)',
        'input_units': 'Input Units',
        'usage_change': 'Change',
        'rate_per_unit': 'Rate per Unit',
        'download_csv': 'Download CSV',
        'preview_result': 'Result',
        'preview_desc': 'Your electricity bill prediction',
        'prediction_date': 'Prediction Date',
        'confidence': 'Confidence',
        'note_break': 'Note: School break may affect usage',
        'validation_warning': 'Warning',
        'error_model_not_found': 'Model not found',
        'error_model_info': 'Please run',
        'efficient_user': 'Efficient User',
        'normal_user': 'Normal User',
        'heavy_user': 'Heavy User',
        'footer': 'Roo-Lot v3.0.0',
        'search_placeholder': 'Search...',
        'calculating': 'Calculating...',
        'try_sample': '📝 Try Sample Data',
    }
}


# ===== Sidebar Component =====
def render_sidebar(lang: str):
    """Render the sidebar navigation"""
    t = TRANSLATIONS[lang]
    
    with st.sidebar:
        # Logo
        st.markdown("""
        <div class="logo-container">
            <div class="logo-icon">💡</div>
            <div class="logo-text">รู้หลอด</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Search
        st.text_input("search", placeholder=t['search_placeholder'], label_visibility="collapsed")
        
        # Navigation Menu
        st.markdown(f'<div class="nav-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="nav-title">Menu</div>', unsafe_allow_html=True)
        
        menu_items = [
            ('📊', t['dashboard'], False),
            ('💳', t['transactions'], False),
            ('💰', t['wallet'], False),
            ('⚡', t['invoice'], True),  # Active
            ('📈', t['budgeting'], False),
            ('📑', t['reports'], False),
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
        
        # Language Toggle
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="nav-title">Language</div>', unsafe_allow_html=True)
        
        lang_col1, lang_col2 = st.columns(2)
        with lang_col1:
            if st.button("🇹🇭 ไทย", use_container_width=True, 
                        type="primary" if lang == 'th' else "secondary"):
                st.session_state.language = 'th'
                st.rerun()
        with lang_col2:
            if st.button("🇺🇸 EN", use_container_width=True,
                        type="primary" if lang == 'en' else "secondary"):
                st.session_state.language = 'en'
                st.rerun()
        
        new_lang = lang
        
        # User Profile
        st.markdown("""
        <div class="user-profile">
            <div class="user-avatar">U</div>
            <div class="user-info">
                <div class="user-name">User</div>
                <div class="user-role">Premium Plan</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        return new_lang


# ===== Main Content Component =====
def render_main_content(t: dict, model: Any):
    """Render the main content area with form"""
    
    # Breadcrumbs
    st.markdown(f'''
    <div class="breadcrumbs">
        Home <span>/</span> {t['invoice']} <span>/</span> <span>{t['predict_next_month']}</span>
    </div>
    ''', unsafe_allow_html=True)
    
    # Page Header
    st.markdown(f'<h1 class="page-title">{t["predict_next_month"]}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="page-subtitle">{t["predict_subtitle"]}</p>', unsafe_allow_html=True)
    
    # Form Section
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="section-header">
        <div class="section-title">{t['usage_details']}</div>
        <div class="section-description">{t['usage_details_desc']}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Wrap inputs in a form to batch updates and improve performance
    with st.form("prediction_form"):
        # Form Inputs
        col1, col2 = st.columns(2)
        
        with col1:
            current_unit = st.number_input(
                t['current_unit'],
                min_value=0, max_value=MAX_UNIT_INPUT, value=150,
                help="Enter units used this month"
            )
            
            people = st.number_input(
                t['people_count'],
                min_value=1, max_value=10, value=2
            )
        
        with col2:
            lag1_unit = st.number_input(
                t['previous_unit'],
                min_value=0, max_value=MAX_UNIT_INPUT, value=140
            )
            
            # Month Selection - Only show next 3 months
            current_month = datetime.datetime.now().month
            current_year = datetime.datetime.now().year
            month_options = []
            for i in range(3):
                next_month = (current_month + i) % 12
                if next_month == 0:
                    next_month = 12
                month_options.append(next_month)
            
            month = st.selectbox(
                t['target_month'],
                options=month_options,
                index=0,  # Default to next month
                format_func=lambda x: datetime.date(2024, x, 1).strftime('%B')
            )
        
        # School Break Toggle
        is_break = st.toggle(t['is_break'], value=False)
        
        # Predict Button (inside form)
        predict_clicked = st.form_submit_button(t['predict_button'], type="primary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        'current_unit': current_unit,
        'lag1_unit': lag1_unit,
        'people': people,
        'month': month,
        'is_break': 1 if is_break else 0
    }, predict_clicked


# ===== Gauge Chart =====
def create_gauge_chart(prediction: float, lang: str) -> go.Figure:
    """Create a beautiful gauge chart for bill visualization"""
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prediction,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={
            'suffix': " ฿" if lang == 'th' else " THB",
            'font': {'size': 36, 'color': '#FFFFFF', 'family': 'Inter, sans-serif'}
        },
        gauge={
            'axis': {
                'range': [None, max(2500, prediction * 1.2)],  # Dynamic range
                'tickwidth': 1,
                'tickcolor': '#707070',
                'tickfont': {'color': '#A0A0A0'}
            },
            'bar': {'color': '#F97316', 'thickness': 0.75},
            'bgcolor': '#1A1A1A',
            'borderwidth': 2,
            'bordercolor': '#333333',
            'steps': [
                {'range': [0, 500], 'color': 'rgba(16, 185, 129, 0.1)'},
                {'range': [500, 1000], 'color': 'rgba(245, 158, 11, 0.1)'},
                {'range': [1000, max(2500, prediction * 1.2)], 'color': 'rgba(239, 68, 68, 0.1)'}
            ],
            'threshold': {
                'line': {'color': '#F97316', 'width': 3},
                'thickness': 0.8,
                'value': prediction
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='#242424',
        plot_bgcolor='#242424',
        font={'color': '#FFFFFF', 'family': 'Inter, sans-serif'},
        height=250,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig


# ===== Preview Panel Component =====
def render_preview_panel(t: dict, prediction: Optional[float] = None, inputs: Optional[dict] = None, lang: str = 'th'):
    """Render the preview panel with results"""
    
    st.markdown(f'<h3 style="margin-bottom: 4px;">{t["preview_result"]}</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #707070; font-size: 13px; margin-bottom: 20px;">{t["preview_desc"]}</p>', 
                unsafe_allow_html=True)
    
    # Preview Card
    st.markdown('<div class="preview-card">', unsafe_allow_html=True)
    
    if prediction is not None and inputs is not None:
        # Gauge Chart
        fig = create_gauge_chart(prediction, lang)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Status Badge
        current = inputs['current_unit']
        if current < 100:
            category = t['low_usage']
            status_class = 'success'
        elif current < 300:
            category = t['moderate_usage']
            status_class = 'warning'
        else:
            category = t['high_usage']
            status_class = 'error'
        
        st.markdown(f'''
        <div style="text-align: center; margin-bottom: 24px;">
            <span class="status-badge {status_class}">{t['usage_category']}: {category}</span>
        </div>
        ''', unsafe_allow_html=True)
        
        # Divider
        st.markdown('<hr style="border: none; border-top: 1px solid #333333; margin: 24px 0;">', 
                    unsafe_allow_html=True)
        
        # Metrics Grid
        change_pct = 0
        if inputs['lag1_unit'] > 0:
            change_pct = ((inputs['current_unit'] - inputs['lag1_unit']) / inputs['lag1_unit']) * 100
        
        rate = prediction / max(inputs['current_unit'], 1)
        
        st.markdown(f'''
        <div class="metrics-grid">
            <div class="metric-item">
                <div class="metric-label">{t['input_units']}</div>
                <div class="metric-value">{inputs['current_unit']} kWh</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">{t['usage_change']}</div>
                <div class="metric-value" style="color: {'#10B981' if change_pct < 0 else '#F59E0B'};">
                    {change_pct:+.1f}%
                </div>
            </div>
            <div class="metric-item">
                <div class="metric-label">{t['rate_per_unit']}</div>
                <div class="metric-value">{rate:.2f} {t['baht']}</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">{t['target_month']}</div>
                <div class="metric-value">{datetime.date(2024, inputs['month'], 1).strftime('%b')}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Note
        if inputs['is_break']:
            st.markdown(f'<p style="color: #707070; font-size: 12px; margin-top: 20px;">💡 {t["note_break"]}</p>',
                        unsafe_allow_html=True)
        
        # Download Button
        export_df = pd.DataFrame({
            'Prediction Date': [datetime.datetime.now().strftime('%Y-%m-%d %H:%M')],
            'Target Month': [datetime.date(2024, inputs['month'], 1).strftime('%B')],
            'Current Unit (kWh)': [inputs['current_unit']],
            'Previous Unit (kWh)': [inputs['lag1_unit']],
            'Number of People': [inputs['people']],
            'School Break': [t['break_yes'] if inputs['is_break'] else t['break_no']],
            'Predicted Bill (THB)': [f"{prediction:.2f}"]
        })
        csv = export_df.to_csv(index=False)
        
        st.download_button(
            label=f"📥 {t['download_csv']}",
            data=csv,
            file_name=f"roolot_prediction_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        # Empty State with Sample Data Button
        st.markdown('''
        <div style="text-align: center; padding: 40px 20px; color: #707070;">
            <div style="font-size: 48px; margin-bottom: 16px;">⚡</div>
            <div style="font-size: 14px;">Fill in the form and click "Predict Bill" to see results</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Sample Data Button
        if st.button(t['try_sample'], use_container_width=True):
            st.session_state.prediction = 1248.50
            st.session_state.prediction_inputs = {
                'current_unit': 250,
                'lag1_unit': 240,
                'people': 3,
                'month': (datetime.datetime.now().month % 12) + 1,
                'is_break': 0
            }
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


# ===== Main Application =====
def main():
    """Main application entry point"""
    
    # Initialize session state
    if 'language' not in st.session_state:
        st.session_state.language = 'th'
    
    if 'prediction' not in st.session_state:
        st.session_state.prediction = None
    
    if 'prediction_inputs' not in st.session_state:
        st.session_state.prediction_inputs = None
    
    lang = st.session_state.language
    t = TRANSLATIONS[lang]
    
    # Create 3-column layout
    sidebar_col, main_col, preview_col = st.columns([1, 3, 2])
    
    # Sidebar
    with st.sidebar:
        new_lang = render_sidebar(lang)
        if new_lang != lang:
            return  # Rerun will happen in render_sidebar
    
    # Load model
    with st.spinner("Loading model..."):
        model = load_model()
    
    if model is None:
        st.error(f"⚠️ {t['error_model_not_found']}")
        st.info(f"{t['error_model_info']}: `python scripts/retrain_v2.py`")
        st.stop()
    
    # Main Content Area
    with main_col:
        inputs, predict_clicked = render_main_content(t, model)
    
    # Handle Prediction
    if predict_clicked:
        is_valid, msg = validate_unit_input(inputs['current_unit'], inputs['lag1_unit'])
        
        if not is_valid:
            st.warning(f"{t['validation_warning']}: {msg}")
        
        input_data = pd.DataFrame({
            'current_unit': [inputs['current_unit']],
            'is_break': [inputs['is_break']],
            'month': [inputs['month']],
            'people': [inputs['people']],
            'lag1_unit': [inputs['lag1_unit']]
        })
        
        try:
            with st.spinner(t['calculating']):
                prediction = predict_with_error_handling(model, input_data)
            
            st.session_state.prediction = prediction
            st.session_state.prediction_inputs = inputs
            st.toast("Prediction successful!", icon="✅")
            
        except PredictionError as e:
            st.error(f"Error: {str(e)}")
    
    # Preview Panel
    with preview_col:
        render_preview_panel(
            t, 
            st.session_state.prediction, 
            st.session_state.prediction_inputs,
            lang
        )
    
    # Footer
    st.markdown("---")
    st.caption(f"{t['footer']} | Dark Professional Dashboard Edition")


if __name__ == "__main__":
    main()
