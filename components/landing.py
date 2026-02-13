"""
Roo-Lot Chatbot - Landing Page Component (Refactored for Robustness)
"""

import streamlit as st

def render_landing_page():
    """Render minimalist landing page with dark theme using native components"""
    
    # CSS for layout and styling
    current_css = """
    <style>
    /* Reset & Layout */
    .landing-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 10vh; /* Approximate vertical centering */
        text-align: center;
        position: relative;
    }
    
    /* Glow Effect */
    .glow-orb {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.15) 0%, transparent 70%);
        border-radius: 50%;
        filter: blur(60px);
        animation: glow 8s ease-in-out infinite;
        z-index: -1;
        pointer-events: none;
    }
    
    /* Logo */
    .landing-logo {
        font-family: var(--font-mono, monospace);
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.1em;
        margin-bottom: 2rem;
        color: #a3a3a3;
    }
    .logo-text { color: #ededed; }
    .logo-tag { color: #3b82f6; }
    
    /* Typography */
    .landing-headline {
        font-family: var(--font-primary, sans-serif);
        font-size: 56px;
        font-weight: 700;
        line-height: 1.1;
        margin-bottom: 1.5rem;
        color: #ededed;  /* Solid light color - highly visible on dark background */
        letter-spacing: -0.03em;
    }
    
    .landing-subheadline {
        font-size: 16px;
        line-height: 1.6;
        color: #a3a3a3;
        margin-bottom: 3rem;
        font-weight: 400;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Metrics */
    .landing-metrics {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 2rem;
        margin-top: 4rem;
        padding-top: 3rem;
        border-top: 1px solid #262626;
    }
    .metric-value {
        font-family: var(--font-mono, monospace);
        font-size: 18px;
        font-weight: 600;
        color: #ededed;
        margin-bottom: 4px;
    }
    .metric-label {
        font-size: 12px;
        color: #737373;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-divider {
        width: 1px;
        height: 32px;
        background-color: #262626;
    }
    
    /* Custom Button Styling override for primary button in this context */
    div[data-testid="stButton"] > button {
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
        transition: all 0.2s ease;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
    }
    
    @keyframes glow {
        0%, 100% { opacity: 0.8; transform: translate(-50%, -50%) scale(1); }
        50% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); }
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .landing-headline { font-size: 36px; }
        .landing-metrics { flex-direction: column; gap: 1rem; }
        .metric-divider { display: none; }
    }
    </style>
    """
    st.markdown(current_css, unsafe_allow_html=True)
    
    # 1. Header Section
    st.markdown("""
    <div class="landing-container">
        <div class="glow-orb"></div>
        <div class="landing-logo">
            <span class="logo-text">ROO-LOT</span>
            <span class="logo-tag">__AI</span>
        </div>
        <h1 class="landing-headline">
            ทำนายค่าไฟฟ้า<br/>
            ด้วย Machine Learning
        </h1>
        <p class="landing-subheadline">
            รู้อะไร ไม่เท่ารู้หลอด – วิเคราะห์การใช้ไฟฟ้าด้วย AI<br/>
            ความแม่นยำ 98.51% · คาดเคลื่อนเฉลี่ย ±71 บาท
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Native Button Section
    # Center the button using columns
    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        start_clicked = st.button("เริ่มวิเคราะห์เลย ➤", type="primary", use_container_width=True)
    
    # 3. Footer/Metrics Section
    st.markdown("""
    <div class="landing-metrics">
        <div class="metric-item">
            <div class="metric-value">R² 0.9888</div>
            <div class="metric-label">Accuracy</div>
        </div>
        <div class="metric-divider"></div>
        <div class="metric-item">
            <div class="metric-value">±61฿</div>
            <div class="metric-label">MAE</div>
        </div>
        <div class="metric-divider"></div>
        <div class="metric-item">
            <div class="metric-value">Random Forest</div>
            <div class="metric-label">Model</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return start_clicked
