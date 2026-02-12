"""
Roo-Lot Chatbot Interface - Phase 2 Complete
Main application with full UI components and styling
"""

import streamlit as st
import time
from pathlib import Path

# Import components
from components.landing import render_landing_page
from components.chat_message import render_message, inject_message_styles
from components.typing_indicator import render_typing_indicator
from components.result_card import render_result_card
from components.sidebar import render_sidebar

# Import utilities
from conversation.manager import ConversationManager
from utils.model_predictor import ElectricityPredictor
from utils.js_injector import inject_smooth_scroll, inject_custom_scrollbar, inject_loading_overlay, inject_quick_reply_styles

# Page configuration
st.set_page_config(
    page_title="Roo-Lot - ทำนายค่าไฟฟ้าด้วย AI",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize managers
@st.cache_resource
def get_conversation_manager():
    return ConversationManager()

@st.cache_resource
def get_predictor():
    return ElectricityPredictor()

conv_manager = get_conversation_manager()
predictor = get_predictor()

# Load global CSS
def load_global_css():
    css_path = Path("assets/styles.css")
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # Inject component styles
    inject_message_styles()
    inject_custom_scrollbar()
    inject_quick_reply_styles()

load_global_css()

def render_chat_interface():
    """Render main chat interface"""
    
    # Render sidebar
    render_sidebar(conv_manager)
    
    # Main chat area
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Chat header
    st.markdown("""
    <div class="chat-header fade-in">
        <div class="chat-header-content">
            <div class="chat-avatar">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M2 17L12 22L22 17" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M2 12L12 17L22 12" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div class="chat-header-info">
                <div class="chat-header-name">Roo-Lot Assistant</div>
                <div class="chat-header-status">
                    <span class="status-indicator"></span>
                    <span>Online</span>
                </div>
            </div>
        </div>
    </div>
    
    <style>
    .chat-header {
        background-color: var(--color-bg-surface);
        border-bottom: 1px solid var(--color-border);
        padding: 16px 24px;
        margin: -1rem -1rem 2rem -1rem;
    }
    
    .chat-header-content {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .chat-avatar {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: var(--color-bg-main);
        border: 1px solid var(--color-border);
        border-radius: 10px;
    }
    
    .chat-header-info {
        flex: 1;
    }
    
    .chat-header-name {
        font-size: 15px;
        font-weight: 600;
        color: var(--color-text-primary);
        margin-bottom: 2px;
    }
    
    .chat-header-status {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        color: var(--color-text-muted);
    }
    
    .status-indicator {
        width: 6px;
        height: 6px;
        background-color: var(--color-accent-green);
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display messages
    messages_container = st.container()
    with messages_container:
        if 'messages' not in st.session_state:
            st.session_state.messages = []
            
        for message in st.session_state.messages:
            render_message(
                role=message["role"],
                content=message["content"],
                timestamp=message["timestamp"]
            )
        
        # Show typing indicator if processing
        if st.session_state.get('is_typing', False):
            render_typing_indicator(duration=0.5)
            st.session_state.is_typing = False
    
    # Check if conversation is complete
    if conv_manager.is_conversation_complete():
        render_results_section()
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Input section
    current_q = conv_manager.get_current_question()
    
    if current_q:
        # Quick reply buttons
        st.markdown('<div class="quick-replies">', unsafe_allow_html=True)
        
        # Ensure quick_replies fallback if key missing
        replies = current_q.get("quick_replies", [])
        if replies:
            cols = st.columns(len(replies) + 1)
            
            for idx, reply in enumerate(replies):
                # Ensure column index sanity
                if idx < len(cols):
                    with cols[idx]:
                        button_label = f"{reply} {current_q.get('unit', '')}"
                        if st.button(button_label, key=f"quick_{current_q['id']}_{idx}", use_container_width=True):
                            st.session_state.is_typing = True
                            # Force manager call
                            conv_manager.process_user_input(reply)
                            time.sleep(0.3)  # Brief delay for UX
                            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Text input form
        with st.form(key=f"input_form_{current_q['id']}", clear_on_submit=True):
            field_label = current_q.get('field', 'Input').replace('_', ' ').title()
            st.markdown(f"""
            <div style="font-size: 13px; color: var(--color-text-muted); margin-bottom: 8px;">
                {field_label}
            </div>
            """, unsafe_allow_html=True)
            
            user_input = st.text_input(
                "Your answer:",
                placeholder=current_q.get("placeholder", ""),
                key=f"user_input_field_{current_q['id']}",
                label_visibility="collapsed"
            )
            
            col1, col2 = st.columns([4, 1])
            with col2:
                submitted = st.form_submit_button("Send →", use_container_width=True, type="primary")
            
            if submitted and user_input:
                st.session_state.is_typing = True
                conv_manager.process_user_input(user_input)
                time.sleep(0.3)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Auto-scroll to bottom
    inject_smooth_scroll()

def render_results_section():
    """Render prediction results section"""
    
    # Make prediction if not already done
    if not st.session_state.get('current_prediction'):
        st.session_state.is_processing = True
        inject_loading_overlay()
        
        with st.spinner(""):
            time.sleep(1.5)  # Simulate processing time for UX
            user_inputs = conv_manager.get_collected_inputs()
            prediction = predictor.predict(user_inputs)
            
            if prediction:
                st.session_state.current_prediction = prediction
                st.session_state.is_processing = False
                
                # Add check for chat_history existence
                if 'chat_history' not in st.session_state:
                    st.session_state.chat_history = []
                
                # Save to history
                st.session_state.chat_history.append({
                    'timestamp': time.strftime("%Y-%m-%d %H:%M"),
                    'predicted_bill': prediction['amount'],
                    'inputs': user_inputs
                })
                
            else:
                st.error("⚠️ เกิดข้อผิดพลาดในการคำนวณ กรุณาลองใหม่อีกครั้ง")
                st.session_state.is_processing = False
                return
        
        st.rerun()
    
    # Display result card
    prediction = st.session_state.current_prediction
    expanded = st.session_state.get('show_detailed_results', False)
    
    # Render card
    render_result_card(prediction, expanded)
    
    # Toggle details button (only if not already expanded via other means, though expander handles it)
    # The dedicated button is redundant if we use st.expander, but let's keep it for explicit control per design
    # Actually, let's just rely on the expander inside render_result_card or use a clean button outside.
    # The render_result_card implementation uses st.expander internally now.
    
    # Divider
    st.markdown('<div style="margin: 2rem 0; border-top: 1px solid var(--color-border);"></div>', unsafe_allow_html=True)
    
    # Follow-up question
    st.markdown("""
    <div class="followup-section fade-in">
        <div class="followup-question">ลองทำนายอีกรอบมั้ยครับ? 🤔</div>
    </div>
    
    <style>
    .followup-section {
        text-align: center;
        padding: 1rem 0;
    }
    
    .followup-question {
        font-size: 16px;
        font-weight: 500;
        color: var(--color-text-primary);
        margin-bottom: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 ลองอีกครั้ง", key="restart_btn", use_container_width=True):
            conv_manager.reset_conversation()
            st.rerun()
    
    with col2:
        if st.button("📝 ปรับค่าเดิม", key="edit_btn", use_container_width=True):
            # For Phase 2, just reset (will implement edit in Phase 4)
            st.info("ฟีเจอร์นี้จะพร้อมใช้งานใน Phase 4")
            time.sleep(1)
            conv_manager.reset_conversation()
            st.rerun()

def main():
    """Main application logic"""
    
    # Initialize session state if not present (critical fix)
    if 'conversation_stage' not in st.session_state:
        st.session_state.conversation_stage = 0
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'user_inputs' not in st.session_state:
        st.session_state.user_inputs = {}
    if 'current_prediction' not in st.session_state:
        st.session_state.current_prediction = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        
    stage = st.session_state.conversation_stage
    
    if stage == 0:
        # Landing page
        if render_landing_page():
            conv_manager.start_conversation()
            st.rerun()
    else:
        # Chat interface (Stage 1 & 2 handled inside)
        render_chat_interface()

if __name__ == "__main__":
    main()
