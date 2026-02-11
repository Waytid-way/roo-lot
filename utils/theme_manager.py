"""
Theme Management System for Roo-Lot v4
Multi-theme support: Dark, Muji, Minimal
Ported from React design system to Streamlit

Author: Roo-Lot Dev Team
Version: 4.0.0 - Modern Multi-Theme Dashboard
"""

import streamlit as st
import json
from typing import Dict, Any
from typing import Literal, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

ThemeOption = Literal["muji", "minimal", "dark"]
LanguageOption = Literal["th", "en"]


@dataclass
class ThemeConfig:
    """Data class for theme configuration"""
    name: str
    description: str
    icon_text: str
    primary_color: str
    bg_color: str
    secondary_bg_color: str
    text_color: str
    font: str = "sans serif"


class ThemeManager:
    """
    Manages application themes and styling
    
    Features:
    - Single Theme: Dark (requested)
    - Custom CSS injection
    - No emoji usage
    - Accessibility compliant (WCAG 2.1 AA)
    - Bilingual support
    """
    
    THEME_CONFIGS: Dict[str, ThemeConfig] = {
        "dark": ThemeConfig(
            name="Dark",
            description="Eye-friendly dark mode",
            icon_text="D",
            primary_color="#00BCD4",
            bg_color="#0E1117",
            secondary_bg_color="#1E2127",
            text_color="#FAFAFA",
            font="sans serif"
        )
    }
    
    @staticmethod
    def get_current_theme() -> ThemeOption:
        """
        Get currently selected theme (Always 'dark')
        
        Returns:
            ThemeOption: 'dark'
        """
        return "dark"
    
    @staticmethod
    def set_theme(theme: ThemeOption) -> None:
        """
        Set theme (No-op as only 'dark' is supported)
        """
        pass
    
    @staticmethod
    def get_theme_config(theme: Optional[ThemeOption] = None) -> ThemeConfig:
        """
        Get configuration for dark theme
        
        Returns:
            ThemeConfig: Theme configuration object
        """
        return ThemeManager.THEME_CONFIGS["dark"]
    
    @staticmethod
    def apply_custom_css() -> None:
        """
        Apply theme-specific custom CSS with enhanced micro-interactions
        
        Features:
        - Custom scrollbar styling
        - Loading spinner customization
        - Button hover effects (Scale & Shadow)
        - Form styling improvements (Borders & Shadows)
        - Responsive design
        - Card hover effects
        """
        config = ThemeManager.get_theme_config()
        
        css = f"""
        <style>
        /* ===== Theme: {config.name} ===== */
        
        /* Root Variables */
        :root {{
            --primary-color: {config.primary_color};
            --bg-color: {config.bg_color};
            --secondary-bg-color: {config.secondary_bg_color};
            --text-color: {config.text_color};
        }}
        
        /* Global App Styling - Ultra Force Dark */
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main, .block-container {{
            background-color: {config.bg_color} !important;
            color: {config.text_color} !important;
        }}
        
        /* Force text color on all common elements */
        h1, h2, h3, h4, h5, h6, p, label, span, div, small {{
            color: {config.text_color} !important;
        }}
        
        /* Specific Fix for Streamlit's new container with border */
        [data-testid="stVerticalBlockBorderWrapper"] > div {{
            background-color: {config.bg_color} !important;
            border-color: rgba(255, 255, 255, 0.1) !important;
        }}
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {config.secondary_bg_color};
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {config.primary_color};
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {config.primary_color}dd;
        }}
        
        /* Loading Spinner Customization */
        .stSpinner > div {{
            border-top-color: {config.primary_color} !important;
        }}
        
        /* Button Enhancements with Micro-interactions */
        .stButton > button {{
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            border-radius: 8px;
            font-weight: 500;
        }}
        
        .stButton > button:hover {{
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        .stButton > button:active {{
            transform: scale(0.98);
        }}
        
        /* Form Styling */
        .stForm {{
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 24px;
            background: {config.bg_color};
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }}
        
        /* Card/Container General Hover Effect */
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {{
            transition: all 0.3s ease;
            border-radius: 8px;
        }}
        
        /* Input Fields */
        /* Improved Input Fields */
        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        div[data-baseweb="base-input"],
        div[data-baseweb="textarea"] > div,
        [data-testid="stNumberInput"] div,
        [data-testid="stTextInput"] div {{
            background-color: {config.secondary_bg_color} !important;
            border-color: rgba(255, 255, 255, 0.1) !important;
            color: {config.text_color} !important;
        }}
        
        input, textarea, select {{
            color: {config.text_color} !important;
            background-color: transparent !important;
            caret-color: {config.primary_color} !important;
        }}
        
        /* Dropdown menu items */
        div[data-baseweb="menu"] {{
            background-color: {config.secondary_bg_color} !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }}
        
        div[data-baseweb="menu"] div {{
            color: {config.text_color} !important;
        }}
        
        input:focus, select:focus, textarea:focus {{
            border-color: {config.primary_color} !important;
            box-shadow: 0 0 0 2px {config.primary_color}33 !important;
        }}
        
        ::placeholder {{
            color: {config.text_color} !important;
            opacity: 0.5 !important;
        }}
        
        /* Divider Styling */
        hr {{
            border-color: {config.secondary_bg_color};
            margin: 2rem 0;
        }}
        
        /* Success/Error/Warning Messages */
        .element-container .stSuccess {{
            background-color: {config.primary_color}15;
            border-left: 4px solid {config.primary_color};
            border-radius: 6px;
            padding: 1rem;
        }}
        
        .element-container .stError {{
            border-radius: 6px;
            padding: 1rem;
        }}
        
        .element-container .stWarning {{
            border-radius: 6px;
            padding: 1rem;
        }}
        
        .element-container .stInfo {{
            border-radius: 6px;
            padding: 1rem;
        }}
        
        /* Sidebar Enhancements */
        [data-testid="stSidebar"] {{
            background-color: {config.secondary_bg_color};
        }}
        
        [data-testid="stSidebar"] .block-container {{
            padding-top: 2rem;
        }}
        
        /* Mobile Responsiveness */
        @media (max-width: 768px) {{
            .stButton > button {{
                width: 100%;
                margin-bottom: 10px;
            }}
            
            /* Larger touch targets for mobile */
            input, select, button {{
                min-height: 44px;
                font-size: 16px; /* Prevents iOS zoom on focus */
            }}
            
            .stForm {{
                padding: 16px;
            }}
        }}
        
        /* Tablet Optimization */
        @media (min-width: 769px) and (max-width: 1024px) {{
            .main .block-container {{
                max-width: 90%;
            }}
        }}
        
        /* Accessibility: Focus Indicators */
        button:focus-visible,
        input:focus-visible,
        select:focus-visible {{
            outline: 2px solid {config.primary_color};
            outline-offset: 2px;
        }}
        
        /* Hide any emoji elements (backup safety) */
        .emoji, [data-emoji] {{
            display: none !important;
        }}
        </style>
        """
        
        st.markdown(css, unsafe_allow_html=True)
    
    @staticmethod
    def get_color_palette() -> Dict[str, str]:
        """
        Get current theme's color palette for use in charts/visualizations
        
        Returns:
            Dict[str, str]: Color palette with keys: primary, background, secondary_bg, text
        """
        config = ThemeManager.get_theme_config()
        return {
            'primary': config.primary_color,
            'background': config.bg_color,
            'secondary_bg': config.secondary_bg_color,
            'text': config.text_color
        }
    
    # ========== Language Management ==========
    
    @staticmethod
    def get_current_language() -> LanguageOption:
        """
        Get currently selected language from session state
        
        Returns:
            LanguageOption: Current language ('th' or 'en')
        """
        if 'language' not in st.session_state:
            st.session_state.language = 'th'  # Default to Thai
        return st.session_state.language
    
    @staticmethod
    def set_language(lang: LanguageOption) -> None:
        """
        Set and persist language selection
        
        Args:
            lang: Language to apply ('th' or 'en')
            
        Raises:
            ValueError: If language is not valid
        """
        if lang not in ['th', 'en']:
            raise ValueError(f"Invalid language: {lang}. Must be 'th' or 'en'")
        st.session_state.language = lang
    
    @staticmethod
    def toggle_language() -> None:
        """Toggle between Thai and English"""
        current = ThemeManager.get_current_language()
        new_lang = 'en' if current == 'th' else 'th'
        ThemeManager.set_language(new_lang)
    
    @staticmethod
    @st.cache_data
    def load_language(lang: LanguageOption) -> Dict[str, str]:
        """
        Load language file from locales directory
        
        Args:
            lang: Language code ('th' or 'en')
            
        Returns:
            Dict[str, str]: Language strings dictionary
            
        Raises:
            FileNotFoundError: If language file doesn't exist
        """
        lang_file = Path(f'locales/{lang}.json')
        
        if not lang_file.exists():
            raise FileNotFoundError(f"Language file not found: {lang_file}")
        
        with open(lang_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def get_text(key: str, default: Optional[str] = None) -> str:
        """
        Get translated text for current language
        
        Args:
            key: Translation key
            default: Default text if key not found
            
        Returns:
            str: Translated text or default or key itself
        """
        lang = ThemeManager.get_current_language()
        translations = ThemeManager.load_language(lang)
        return translations.get(key, default or key)
    
    @staticmethod
    def render_language_toggle() -> None:
        """
        Render language toggle button in header
        
        Features:
        - Shows current language flag/code
        - One-click toggle between TH and EN
        - Positioned in top-right corner
        """
        current_lang = ThemeManager.get_current_language()
        
        # Language display
        lang_display = {
            'th': 'TH',
            'en': 'EN'
        }
        
        # Create button in sidebar or main area
        col1, col2 = st.columns([0.85, 0.15])
        
        with col2:
            button_label = f"Lang: {lang_display[current_lang]}"
            if st.button(button_label, key="language_toggle", use_container_width=True):
                ThemeManager.toggle_language()
                st.rerun()

