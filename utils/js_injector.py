"""
Roo-Lot Chatbot - JavaScript Injector
"""

import streamlit as st
import streamlit.components.v1 as components

def inject_smooth_scroll():
    """Inject JavaScript for smooth auto-scrolling to latest message"""
    
    components.html("""
    <script>
    // Auto-scroll to bottom of chat container
    function scrollToBottom() {
        const chatContainer = window.parent.document.querySelector('[data-testid="stVerticalBlock"]');
        if (chatContainer) {
            chatContainer.scrollTo({
                top: chatContainer.scrollHeight,
                behavior: 'smooth'
            });
        }
    }
    
    // Call on load
    window.addEventListener('load', () => {
        setTimeout(scrollToBottom, 300);
    });
    
    // Listen for new messages
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length) {
                setTimeout(scrollToBottom, 100);
            }
        });
    });
    
    // Observe main container
    const targetNode = window.parent.document.querySelector('[data-testid="stVerticalBlock"]');
    if (targetNode) {
        observer.observe(targetNode, {
            childList: true,
            subtree: true
        });
    }
    </script>
    """, height=0)

def inject_custom_scrollbar():
    """Inject custom scrollbar styles"""
    
    st.markdown("""
    <style>
    /* Custom scrollbar for chat container */
    [data-testid="stVerticalBlock"]::-webkit-scrollbar {
        width: 6px;
    }
    
    [data-testid="stVerticalBlock"]::-webkit-scrollbar-track {
        background: var(--color-bg-main);
    }
    
    [data-testid="stVerticalBlock"]::-webkit-scrollbar-thumb {
        background: var(--color-bg-surface);
        border-radius: 3px;
    }
    
    [data-testid="stVerticalBlock"]::-webkit-scrollbar-thumb:hover {
        background: #2a2a2a;
    }
    </style>
    """, unsafe_allow_html=True)

def inject_loading_overlay():
    """Inject loading overlay for predictions"""
    
    if st.session_state.get('is_processing', False):
        st.markdown("""
        <div class="loading-overlay">
            <div class="loading-spinner">
                <div class="spinner-ring"></div>
                <div class="spinner-text">กำลังคำนวณ...</div>
            </div>
        </div>
        
        <style>
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(10, 10, 10, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            animation: fadeIn 0.3s ease-out;
        }
        
        .loading-spinner {
            text-align: center;
        }
        
        .spinner-ring {
            width: 60px;
            height: 60px;
            margin: 0 auto 20px;
            border: 3px solid var(--color-border);
            border-top-color: var(--color-accent-blue);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        .spinner-text {
            font-family: var(--font-mono);
            font-size: 14px;
            color: var(--color-text-secondary);
        }
        
        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }
        </style>
        """, unsafe_allow_html=True)

def inject_quick_reply_styles():
    """Inject styles for quick reply buttons"""
    
    st.markdown("""
    <style>
    /* Quick reply container */
    .quick-replies {
        display: flex;
        gap: 8px;
        margin: 16px 0;
        flex-wrap: wrap;
    }
    
    /* Quick reply button */
    .quick-reply-btn {
        background-color: transparent;
        border: 1px solid var(--color-border);
        border-radius: 20px;
        padding: 8px 16px;
        font-size: 13px;
        font-family: var(--font-mono);
        color: var(--color-text-secondary);
        cursor: pointer;
        transition: all var(--transition-fast);
    }
    
    .quick-reply-btn:hover {
        background-color: var(--color-bg-surface);
        border-color: var(--color-accent-blue);
        color: var(--color-accent-blue);
        transform: translateY(-1px);
    }
    
    .quick-reply-btn:active {
        transform: translateY(0);
    }
    </style>
    """, unsafe_allow_html=True)
