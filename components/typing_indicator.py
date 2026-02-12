"""
Roo-Lot Chatbot - Typing Indicator Component
"""

import streamlit as st
import time

def render_typing_indicator(duration: float = 1.0):
    """
    Render typing indicator animation
    
    Args:
        duration: How long to show the indicator (seconds)
    """
    
    # Render typing animation
    typing_html = st.markdown("""
    <div class="typing-indicator-container">
        <div class="message-avatar">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    </div>
    
    <style>
    .typing-indicator-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 16px 0;
        animation: fadeIn 0.3s ease-out;
    }
    
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 12px 16px;
        background-color: var(--color-bg-surface);
        border: 1px solid var(--color-border);
        border-radius: 12px;
    }
    
    .typing-dot {
        width: 6px;
        height: 6px;
        background-color: var(--color-text-secondary);
        border-radius: 50%;
        animation: typingPulse 1.4s ease-in-out infinite;
    }
    
    .typing-dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typingPulse {
        0%, 60%, 100% {
            opacity: 0.3;
            transform: scale(1);
        }
        30% {
            opacity: 1;
            transform: scale(1.2);
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Wait for duration
    time.sleep(duration)
    
    # Clear the typing indicator
    typing_html.empty()
