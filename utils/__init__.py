"""
Roo-Lot Chatbot - Utilities Module
"""

from .model_predictor import ElectricityPredictor
from .js_injector import (
    inject_smooth_scroll,
    inject_custom_scrollbar,
    inject_loading_overlay,
    inject_quick_reply_styles
)

__all__ = [
    'ElectricityPredictor',
    'inject_smooth_scroll',
    'inject_custom_scrollbar',
    'inject_loading_overlay',
    'inject_quick_reply_styles'
]
