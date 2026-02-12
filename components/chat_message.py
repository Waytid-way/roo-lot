"""
Roo-Lot Chatbot - Chat Message Component
"""

import streamlit as st

def render_message(role: str, content: str, timestamp: str):
    """
    Render a chat message bubble
    
    Args:
        role: 'bot' or 'user'
        content: Message text
        timestamp: Time string (HH:MM)
    """
    
    if role == "assistant" or role == "bot":
        # Bot message with subtle background
        st.markdown(f"""
        <div class="message-container bot-message slide-up">
            <div class="message-avatar">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M2 17L12 22L22 17" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M2 12L12 17L22 12" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div class="message-content">
                <div class="message-text">{content}</div>
                <div class="message-timestamp">{timestamp}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # User message with ghost styling (no background)
        st.markdown(f"""
        <div class="message-container user-message slide-up">
            <div class="message-content">
                <div class="message-text">{content}</div>
                <div class="message-timestamp">{timestamp}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def inject_message_styles():
    """Inject CSS styles for chat messages"""
    st.markdown("""
    <style>
    .message-container {
        display: flex;
        gap: 12px;
        margin: 16px 0;
        max-width: 100%;
    }
    
    /* Bot message (left-aligned) */
    .bot-message {
        justify-content: flex-start;
    }
    
    .bot-message .message-content {
        background-color: var(--color-bg-surface);
        border: 1px solid var(--color-border);
    }
    
    /* User message (right-aligned, ghost style) */
    .user-message {
        justify-content: flex-end;
    }
    
    .user-message .message-content {
        background-color: transparent;
        border: 1px solid var(--color-border);
    }
    
    /* Avatar */
    .message-avatar {
        width: 32px;
        height: 32px;
        min-width: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: var(--color-bg-surface);
        border: 1px solid var(--color-border);
        border-radius: 8px;
    }
    
    /* Content */
    .message-content {
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 12px;
        transition: all var(--transition-fast);
    }
    
    .message-content:hover {
        border-color: var(--color-border-hover);
    }
    
    /* Text */
    .message-text {
        font-size: 14px;
        line-height: 1.6;
        color: var(--color-text-primary);
        margin-bottom: 4px;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    /* Timestamp */
    .message-timestamp {
        font-size: 11px;
        color: var(--color-text-muted);
        font-family: var(--font-mono);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .message-content {
            max-width: 85%;
        }
    }
    </style>
    """, unsafe_allow_html=True)
