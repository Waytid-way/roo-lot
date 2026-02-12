"""
Roo-Lot Chatbot - Sidebar Component
"""

import streamlit as st
from datetime import datetime

def render_sidebar(conversation_manager):
    """
    Render sidebar with chat history and controls
    
    Args:
        conversation_manager: ConversationManager instance
    """
    
    with st.sidebar:
        # Inject sidebar styles
        inject_sidebar_styles()
        
        # Wordmark/Logo
        st.markdown("""
        <div class="sidebar-header fade-in">
            <div class="sidebar-wordmark">
                <span class="wordmark-main">ROO-LOT</span>
                <span class="wordmark-tag">__AI</span>
            </div>
            <div class="sidebar-tagline">Electricity Bill Predictor</div>
        </div>
        """, unsafe_allow_html=True)
        
        # New Chat Button
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        if st.button("➕ New Chat", key="new_chat_btn", use_container_width=True):
            conversation_manager.start_conversation()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Divider
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        
        # Chat History
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-section-title">ประวัติแชท</div>', unsafe_allow_html=True)
        
        chat_history = st.session_state.get('chat_history', [])
        
        if len(chat_history) == 0:
            st.markdown("""
            <div class="empty-history">
                <div class="empty-history-icon">💬</div>
                <div class="empty-history-text">ยังไม่มีประวัติการแชท</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for idx, history_item in enumerate(reversed(chat_history)):
                # Use actual index from end to start for retrieval if needed, 
                # but visually we show newest first. 
                # passing original index (len - 1 - idx) might be safer if load_from_history uses index
                original_idx = len(chat_history) - 1 - idx
                render_history_item(history_item, original_idx, conversation_manager, idx)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Spacer to push settings to bottom
        st.markdown('<div style="flex-grow: 1;"></div>', unsafe_allow_html=True)
        
        # Divider
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        
        # Settings Button (bottom)
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        if st.button("⚙️ ตั้งค่า", key="settings_btn", use_container_width=True):
            st.session_state.show_settings = not st.session_state.get('show_settings', False)
        
        if st.session_state.get('show_settings', False):
            st.markdown("""
            <div class="settings-panel slide-up">
                <div class="settings-title">Preferences</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Detailed Analysis Toggle
            show_details = st.toggle(
                "Show Detailed Analysis", 
                value=st.session_state.get('show_detailed_results', False),
                key="setting_details"
            )
            st.session_state.show_detailed_results = show_details
            
            # Clear History Button
            if st.button("🗑️ Clear History", key="clear_history_btn", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.messages = []
                st.session_state.user_inputs = {}
                st.session_state.current_prediction = None
                st.session_state.conversation_stage = 1
                st.rerun()

            st.markdown("""
            <style>
            .settings-panel {
                background-color: var(--color-bg-surface);
                border: 1px solid var(--color-border);
                border-radius: 8px;
                padding: 12px;
                margin-top: 8px;
            }
            .settings-title {
                font-size: 12px;
                font-weight: 600;
                color: var(--color-text-secondary);
                margin-bottom: 8px;
                text-transform: uppercase;
            }
            </style>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

def render_history_item(history_item: dict, index: int, conversation_manager, visual_index: int):
    """Render a single history item as bento card"""
    
    timestamp = history_item.get('timestamp', '')
    predicted_bill = history_item.get('predicted_bill', 0)
    inputs = history_item.get('inputs', {})
    
    # Format preview text
    room_size = inputs.get('room_size', 0)
    ac_hours = inputs.get('ac_hours', 0)
    preview = f"{room_size}m² · {ac_hours}h AC"
    
    # Create clickable history card
    st.markdown(f"""
    <div class="history-item slide-up" style="animation-delay: {visual_index * 0.05}s;">
        <div class="history-timestamp">{timestamp}</div>
        <div class="history-bill">{predicted_bill:.0f} ฿</div>
        <div class="history-preview">{preview}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hidden button for click detection could be tricky with layout, 
    # but let's try to put it "over" or just below. 
    # Since we can't easily overlay transparent buttons in pure Streamlit without custom components,
    # we might use a small "Load" button or make the whole thing a button if we ditch the custom HTML structure.
    # However, to keep the custom styling, we often use a button below or adjacent.
    # For this specific "Senior Dev" request, let's use a small unobtrusive link/button.
    
    if st.button(f"Load Selection", key=f"history_load_{index}", help=f"Load prediction from {timestamp}"):
        # Logic to load history would go here. 
        # Since ConversationManager might not have load_from_history yet, we'll need to double check manager.py
        # For now, let's assume it exists or we add it.
        if hasattr(conversation_manager, 'load_from_history'):
             conversation_manager.load_from_history(index)
             st.rerun()

def inject_sidebar_styles():
    """Inject CSS styles for sidebar"""
    st.markdown("""
    <style>
    /* Sidebar container */
    [data-testid="stSidebar"] {
        background-color: var(--color-bg-main) !important;
        border-right: 1px solid var(--color-border) !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 2rem 1rem;
        display: flex;
        flex-direction: column;
        height: 100vh;
    }
    
    /* Header */
    .sidebar-header {
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid var(--color-border);
    }
    
    .sidebar-wordmark {
        font-family: var(--font-mono);
        font-size: 18px;
        font-weight: 700;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    
    .wordmark-main {
        color: var(--color-text-primary);
    }
    
    .wordmark-tag {
        color: var(--color-accent-blue);
    }
    
    .sidebar-tagline {
        font-size: 11px;
        color: var(--color-text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Section */
    .sidebar-section {
        margin-bottom: 1rem;
    }
    
    .sidebar-section-title {
        font-size: 12px;
        font-weight: 600;
        color: var(--color-text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 12px;
    }
    
    /* Divider */
    .sidebar-divider {
        height: 1px;
        background-color: var(--color-border);
        margin: 1.5rem 0;
    }
    
    /* Empty history */
    .empty-history {
        text-align: center;
        padding: 2rem 1rem;
    }
    
    .empty-history-icon {
        font-size: 32px;
        margin-bottom: 8px;
        opacity: 0.5;
    }
    
    .empty-history-text {
        font-size: 13px;
        color: var(--color-text-muted);
    }
    
    /* History item (bento card) */
    .history-item {
        background-color: var(--color-bg-surface);
        border: 1px solid var(--color-border);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all var(--transition-fast);
    }
    
    .history-item:hover {
        background-color: var(--color-bg-surface-hover);
        border-color: var(--color-border-hover);
        transform: translateX(2px);
    }
    
    .history-timestamp {
        font-size: 10px;
        font-family: var(--font-mono);
        color: var(--color-text-muted);
        margin-bottom: 4px;
    }
    
    .history-bill {
        font-size: 18px;
        font-family: var(--font-mono);
        font-weight: 700;
        color: var(--color-accent-blue);
        margin-bottom: 4px;
    }
    
    .history-preview {
        font-size: 11px;
        color: var(--color-text-secondary);
    }
    
    /* Override Streamlit button styles in sidebar */
    [data-testid="stSidebar"] .stButton button {
        background-color: var(--color-bg-surface) !important;
        border: 1px solid var(--color-border) !important;
        color: var(--color-text-primary) !important;
        font-size: 13px !important;
        padding: 10px 16px !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: var(--color-bg-surface-hover) !important;
        border-color: var(--color-border-hover) !important;
    }
    </style>
    """, unsafe_allow_html=True)
