"""
Theme System for Roo-Lot v4 - Modern Multi-Theme Dashboard
Provides 3 themes: Dark, Muji, Minimal
Ported from React design system to Streamlit

Author: Roo-Lot Dev Team
Version: 4.0.0
"""

from typing import Dict, Any

# ===== Theme Definitions =====
THEMES = {
    'dark': {
        'name': 'Dark',
        'icon': '🌙',
        'colors': {
            # Backgrounds
            'bg_primary': '#0a0a0a',
            'bg_secondary': '#121212',
            'bg_card': '#121212',
            'bg_input': '#1a1a1a',
            'bg_elevated': '#1e1e1e',
            
            # Text
            'text_primary': '#e5e5e5',
            'text_heading': '#ffffff',
            'text_muted': '#9ca3af',
            'text_secondary': '#6b7280',
            
            # Accent
            'accent_primary': '#06b6d4',  # Cyan
            'accent_hover': '#22d3ee',
            'accent_bg': '#06b6d4',
            'accent_muted': 'rgba(6, 182, 212, 0.1)',
            
            # Borders
            'border_default': '#1f2937',
            'border_accent': '#06b6d4',
            
            # Status Colors
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444',
            'info': '#3b82f6',
            
            # Gauge
            'gauge_base': '#333333',
            'gauge_fill': '#06b6d4',
        }
    },
    
    'muji': {
        'name': 'Muji',
        'icon': '☕',
        'colors': {
            # Backgrounds (Warm, Natural)
            'bg_primary': '#F5F1E8',
            'bg_secondary': '#EAE4D9',
            'bg_card': '#FFFFFF',
            'bg_input': '#FAF9F6',
            'bg_elevated': '#FFFFFF',
            
            # Text
            'text_primary': '#5C5C5C',
            'text_heading': '#4A4A4A',
            'text_muted': '#8C8C8C',
            'text_secondary': '#9E9E9E',
            
            # Accent (Terracotta)
            'accent_primary': '#C77B58',
            'accent_hover': '#D68C6A',
            'accent_bg': '#C77B58',
            'accent_muted': 'rgba(199, 123, 88, 0.1)',
            
            # Borders
            'border_default': '#D4C5B0',
            'border_accent': '#C77B58',
            
            # Status Colors
            'success': '#7BA05B',
            'warning': '#E89E3C',
            'error': '#C55A5A',
            'info': '#6B8CAE',
            
            # Gauge
            'gauge_base': '#E0D6C8',
            'gauge_fill': '#C77B58',
        }
    },
    
    'minimal': {
        'name': 'Minimal',
        'icon': '🌿',
        'colors': {
            # Backgrounds (Clean White)
            'bg_primary': '#FFFFFF',
            'bg_secondary': '#F8F9FA',
            'bg_card': '#FFFFFF',
            'bg_input': '#F1F3F5',
            'bg_elevated': '#FFFFFF',
            
            # Text
            'text_primary': '#495057',
            'text_heading': '#212529',
            'text_muted': '#ADB5BD',
            'text_secondary': '#6C757D',
            
            # Accent (Green)
            'accent_primary': '#2E7D32',
            'accent_hover': '#388E3C',
            'accent_bg': '#2E7D32',
            'accent_muted': 'rgba(46, 125, 50, 0.1)',
            
            # Borders
            'border_default': '#E9ECEF',
            'border_accent': '#2E7D32',
            
            # Status Colors
            'success': '#28A745',
            'warning': '#FFC107',
            'error': '#DC3545',
            'info': '#17A2B8',
            
            # Gauge
            'gauge_base': '#E9ECEF',
            'gauge_fill': '#2E7D32',
        }
    }
}


def generate_css(theme_name: str = 'dark') -> str:
    """
    Generate complete CSS for the selected theme
    Returns CSS string with all custom properties and component styles
    """
    
    theme = THEMES.get(theme_name, THEMES['dark'])
    colors = theme['colors']
    
    css = f"""
<style>
/* ========================================
   Theme: {theme['name']} - Roo-Lot v4
   ======================================== */

/* Import Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Prompt:wght@400;500;600;700&display=swap');

/* CSS Variables - Theme Colors */
:root {{
    /* Backgrounds */
    --bg-primary: {colors['bg_primary']};
    --bg-secondary: {colors['bg_secondary']};
    --bg-card: {colors['bg_card']};
    --bg-input: {colors['bg_input']};
    --bg-elevated: {colors['bg_elevated']};
    
    /* Text */
    --text-primary: {colors['text_primary']};
    --text-heading: {colors['text_heading']};
    --text-muted: {colors['text_muted']};
    --text-secondary: {colors['text_secondary']};
    
    /* Accent */
    --accent-primary: {colors['accent_primary']};
    --accent-hover: {colors['accent_hover']};
    --accent-bg: {colors['accent_bg']};
    --accent-muted: {colors['accent_muted']};
    
    /* Borders */
    --border-default: {colors['border_default']};
    --border-accent: {colors['border_accent']};
    
    /* Status */
    --success: {colors['success']};
    --warning: {colors['warning']};
    --error: {colors['error']};
    --info: {colors['info']};
    
    /* Gauge */
    --gauge-base: {colors['gauge_base']};
    --gauge-fill: {colors['gauge_fill']};
    
    /* Typography */
    --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-thai: 'Prompt', 'Noto Sans Thai', sans-serif;
}}

/* ========================================
   Global Styles
   ======================================== */

* {{
    font-family: var(--font-primary);
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}}

html, body, [data-testid="stAppViewContainer"] {{
    background-color: var(--bg-primary) !important;
}}

[data-testid="stHeader"] {{
    display: none;
}}

[data-testid="stToolbar"] {{
    display: none;
}}

/* Main Content Area */
.main .block-container {{
    padding-top: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 100% !important;
}}

/* ========================================
   Sidebar Styling
   ======================================== */

[data-testid="stSidebar"] {{
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-default);
}}

[data-testid="stSidebar"] > div:first-child {{
    padding: 24px 16px !important;
}}

/* Logo Container */
.logo-container {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0 8px 24px 8px;
    border-bottom: 1px solid var(--border-default);
    margin-bottom: 24px;
}}

.logo-icon {{
    width: 40px;
    height: 40px;
    background: var(--accent-primary);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}}

.logo-text {{
    font-family: var(--font-thai);
    font-size: 20px;
    font-weight: 600;
    color: var(--text-heading);
}}

/* Navigation */
.nav-section {{
    margin-bottom: 24px;
}}

.nav-title {{
    font-size: 10px;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 0 8px;
    margin-bottom: 12px;
}}

.nav-item {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-bottom: 4px;
    font-size: 14px;
    color: var(--text-secondary);
    text-decoration: none;
}}

.nav-item:hover {{
    background: var(--bg-input);
    color: var(--text-heading);
    transform: translateX(2px);
}}

.nav-item.active {{
    background: var(--accent-muted);
    color: var(--accent-primary);
    font-weight: 500;
    border: 1px solid var(--border-accent);
}}

.nav-icon {{
    font-size: 18px;
}}

/* ========================================
   Card Components
   ======================================== */

.card {{
    background: var(--bg-card);
    border: 1px solid var(--border-default);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}}

.card:hover {{
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}}

.card-header {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border-default);
}}

.card-icon {{
    color: var(--accent-primary);
    font-size: 18px;
}}

.card-title {{
    font-family: var(--font-thai);
    font-size: 18px;
    font-weight: 600;
    color: var(--text-heading);
}}

.card-description {{
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 4px;
}}

/* ========================================
   Form Inputs
   ======================================== */

.stTextInput input,
.stNumberInput input,
.stSelectbox select,
.stDateInput input,
.stTimeInput input {{
    background-color: var(--bg-input) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    color: var(--text-primary) !important;
    font-size: 14px !important;
    transition: all 0.2s ease !important;
}}

.stTextInput input:focus,
.stNumberInput input:focus,
.stSelectbox select:focus,
.stDateInput input:focus,
.stTimeInput input:focus {{
    border-color: var(--border-accent) !important;
    box-shadow: 0 0 0 3px var(--accent-muted) !important;
}}

/* Input Labels */
.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stDateInput label,
.stTimeInput label {{
    font-family: var(--font-thai) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    margin-bottom: 6px !important;
}}

/* Input Container Styling */
.input-container {{
    background: var(--bg-input);
    border: 1px solid var(--border-default);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
}}

/* ========================================
   Buttons
   ======================================== */

.stButton > button {{
    background: transparent !important;
    border: 1px solid var(--border-default) !important;
    color: var(--text-primary) !important;
    padding: 10px 20px !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}}

.stButton > button:hover {{
    background: var(--bg-input) !important;
    transform: translateY(-1px);
}}

.stButton > button[kind="primary"] {{
    background: var(--accent-bg) !important;
    border: none !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
}}

.stButton > button[kind="primary"]:hover {{
    background: var(--accent-hover) !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15) !important;
}}

.stButton > button[kind="primary"]:active {{
    transform: scale(0.98);
}}

/* Form Submit Button (inside st.form) */
.stButton button[type="submit"] {{
    width: 100%;
    background: var(--accent-bg) !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 14px 24px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
}}

.stButton button[type="submit"]:hover {{
    background: var(--accent-hover) !important;
    transform: translateY(-2px);
}}

/* ========================================
   Toggle/Checkbox
   ======================================== */

.stCheckbox {{
    padding: 12px;
    background: var(--bg-input);
    border-radius: 8px;
    margin-bottom: 8px;
}}

.stCheckbox label {{
    color: var(--text-heading) !important;
    font-weight: 500 !important;
    font-size: 14px !important;
}}

.stCheckbox input[type="checkbox"] {{
    accent-color: var(--accent-primary) !important;
}}

/* ========================================
   Status Badges
   ======================================== */

.status-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.status-badge.success {{
    background: rgba(16, 185, 129, 0.1);
    color: var(--success);
    border: 1px solid var(--success);
}}

.status-badge.warning {{
    background: rgba(245, 158, 11, 0.1);
    color: var(--warning);
    border: 1px solid var(--warning);
}}

.status-badge.error {{
    background: rgba(239, 68, 68, 0.1);
    color: var(--error);
    border: 1px solid var(--error);
}}

.status-badge.info {{
    background: rgba(59, 130, 246, 0.1);
    color: var(--info);
    border: 1px solid var(--info);
}}

/* ========================================
   Table Styling
   ======================================== */

.history-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}}

.history-table thead {{
    background: var(--bg-input);
    color: var(--text-muted);
    font-size: 10px;
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.5px;
}}

.history-table th {{
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid var(--border-default);
    font-weight: 600;
}}

.history-table td {{
    padding: 14px 16px;
    border-bottom: 1px solid var(--border-default);
    color: var(--text-primary);
}}

.history-table tbody tr {{
    transition: background-color 0.2s ease;
}}

.history-table tbody tr:hover {{
    background: var(--bg-input);
}}

.history-table .timestamp {{
    font-family: 'Courier New', monospace;
    color: var(--text-muted);
    font-size: 12px;
}}

/* ========================================
   Toast Notification
   ======================================== */

.toast {{
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    background: var(--bg-card);
    border: 1px solid var(--border-accent);
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    display: flex;
    align-items: center;
    gap: 12px;
    animation: slideIn 0.3s ease-out;
    max-width: 400px;
}}

@keyframes slideIn {{
    from {{
        transform: translateX(100%);
        opacity: 0;
    }}
    to {{
        transform: translateX(0);
        opacity: 1;
    }}
}}

.toast-icon {{
    color: var(--success);
    font-size: 20px;
}}

.toast-content {{
    flex: 1;
}}

.toast-title {{
    color: var(--text-heading);
    font-weight: 600;
    font-size: 14px;
    margin-bottom: 4px;
}}

.toast-desc {{
    color: var(--text-muted);
    font-size: 12px;
}}

/* ========================================
   Metrics & Stats
   ======================================== */

.metric-card {{
    background: var(--bg-input);
    border: 1px solid var(--border-default);
    border-radius: 12px;
    padding: 16px;
    transition: all 0.2s ease;
}}

.metric-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}}

.metric-label {{
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}}

.metric-value {{
    font-size: 24px;
    font-weight: 700;
    color: var(--text-heading);
}}

.metric-unit {{
    font-size: 14px;
    color: var(--text-muted);
    margin-left: 4px;
}}

/* ========================================
   Result/Gauge Display
   ======================================== */

.result-container {{
    text-align: center;
    padding: 40px 20px;
}}

.result-value {{
    font-size: 48px;
    font-weight: 700;
    color: var(--text-heading);
    letter-spacing: -1px;
    margin: 20px 0 8px 0;
}}

.result-unit {{
    font-size: 12px;
    color: var(--text-muted);
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 1px;
}}

.result-status {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-top: 16px;
    padding: 8px 16px;
    background: var(--accent-muted);
    border-radius: 20px;
    font-size: 11px;
    color: var(--accent-primary);
    font-weight: 600;
}}

.confidence-indicator {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 16px;
}}

.confidence-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--success);
    animation: pulse 2s infinite;
}}

@keyframes pulse {{
    0%, 100% {{
        opacity: 1;
    }}
    50% {{
        opacity: 0.5;
    }}
}}

/* ========================================
   Theme Selector
   ======================================== */

.theme-selector {{
    display: flex;
    gap: 8px;
    padding: 12px;
    background: var(--bg-input);
    border-radius: 12px;
    margin-bottom: 16px;
}}

.theme-button {{
    flex: 1;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid transparent;
    cursor: pointer;
    transition: all 0.2s ease;
    background: transparent;
    text-align: center;
    font-size: 20px;
}}

.theme-button:hover {{
    background: var(--bg-card);
    transform: scale(1.05);
}}

.theme-button.active {{
    border-color: var(--border-accent);
    background: var(--bg-card);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}}

/* ========================================
   Spinner & Loading
   ======================================== */

.stSpinner > div {{
    border-color: var(--accent-primary) !important;
}}

/* ========================================
   Empty State
   ======================================== */

.empty-state {{
    text-align: center;
    padding: 60px 20px;
    color: var(--text-muted);
}}

.empty-state-icon {{
    font-size: 48px;
    margin-bottom: 16px;
    opacity: 0.5;
}}

.empty-state-text {{
    font-size: 14px;
    color: var(--text-muted);
}}

/* ========================================
   Scrollbar
   ======================================== */

::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}

::-webkit-scrollbar-track {{
    background: var(--bg-primary);
}}

::-webkit-scrollbar-thumb {{
    background: var(--border-default);
    border-radius: 4px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: var(--text-muted);
}}

/* ========================================
   Responsive Design
   ======================================== */

@media (max-width: 768px) {{
    .card {{
        padding: 16px;
    }}
    
    .result-value {{
        font-size: 36px;
    }}
    
    .main .block-container {{
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}
}}

/* ========================================
   Utility Classes
   ======================================== */

.text-center {{
    text-align: center;
}}

.mt-4 {{
    margin-top: 16px;
}}

.mb-4 {{
    margin-bottom: 16px;
}}

.p-4 {{
    padding: 16px;
}}

.rounded {{
    border-radius: 8px;
}}

.shadow {{
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}}

</style>
"""
    
    return css


def get_theme_info(theme_name: str) -> Dict[str, Any]:
    """Get theme metadata"""
    return THEMES.get(theme_name, THEMES['dark'])


def get_theme_colors(theme_name: str) -> Dict[str, str]:
    """Get color palette for a theme"""
    theme = THEMES.get(theme_name, THEMES['dark'])
    return theme['colors']


def get_available_themes() -> list:
    """Get list of available theme names"""
    return list(THEMES.keys())
