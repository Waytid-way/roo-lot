"""
Roo-Lot Chatbot - Result Card Component
"""

import streamlit as st
import plotly.graph_objects as go
from utils.exporter import create_pdf_report

def render_result_card(prediction_data: dict, expanded: bool = False):
    """
    Render prediction result card with data HUD aesthetic
    
    Args:
        prediction_data: Dictionary with prediction results
        expanded: Whether to show detailed view
    """
    
    amount = prediction_data['amount']
    range_val = prediction_data['range']
    # Add fallback for missing keys, just in case
    breakdown = prediction_data.get('breakdown', {
        'ac_cost': amount * 0.6,
        'appliances_cost': amount * 0.3,
        'base_fee': amount * 0.1
    })
    metrics = prediction_data.get('model_metrics', {
        'r2_score': 0.9923,
        'mae': 43.63,
        'rmse': 58.41
    })
    
    # CSS Styles (Non-f-string to avoid brace conflict)
    st.markdown("""
    <style>
    .result-card {
        background-color: var(--color-bg-surface);
        border: 1px solid var(--color-border);
        border-radius: 16px;
        padding: 24px;
        margin: 24px 0;
        cursor: pointer;
        transition: all var(--transition-base);
    }
    
    .result-card:hover {
        border-color: var(--color-border-hover);
        transform: translateY(-2px);
    }
    
    /* Header */
    .result-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 20px;
    }
    
    .result-icon {
        font-size: 20px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .result-label {
        font-family: var(--font-mono);
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.1em;
        color: var(--color-text-muted);
    }
    
    /* Main Amount */
    .result-amount {
        display: flex;
        align-items: baseline;
        gap: 8px;
        margin-bottom: 8px;
    }
    
    .amount-value {
        font-family: var(--font-mono);
        font-size: 56px;
        font-weight: 700;
        background: linear-gradient(135deg, var(--color-accent-blue) 0%, var(--color-accent-green) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
    }
    
    .amount-unit {
        font-family: var(--font-mono);
        font-size: 20px;
        font-weight: 600;
        color: var(--color-text-secondary);
    }
    
    /* Range */
    .result-range {
        font-size: 14px;
        color: var(--color-text-secondary);
        margin-bottom: 24px;
        font-family: var(--font-mono);
    }
    
    /* Stats Grid */
    .result-stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-bottom: 20px;
        padding-top: 20px;
        border-top: 1px solid var(--color-border);
    }
    
    .stat-cell {
        text-align: center;
    }
    
    .stat-value {
        font-family: var(--font-mono);
        font-size: 18px;
        font-weight: 600;
        color: var(--color-text-primary);
        margin-bottom: 4px;
    }
    
    .stat-label {
        font-size: 11px;
        color: var(--color-text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Expand CTA */
    .result-expand-cta {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding-top: 16px;
        border-top: 1px solid var(--color-border);
        font-size: 13px;
        color: var(--color-text-secondary);
        transition: color var(--transition-fast);
    }
    
    .result-card:hover .result-expand-cta {
        color: var(--color-accent-blue);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .amount-value {
            font-size: 40px;
        }
        
        .result-stats-grid {
            grid-template-columns: 1fr;
            gap: 12px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Content (f-string) - NO INDENTATION to prevent Markdown code block interpretation
    st.markdown(f"""<div class="result-card scale-in">
<div class="result-header">
<div class="result-icon">⚡</div>
<div class="result-label">ELECTRICITY BILL PREDICTION</div>
</div>
<div class="result-amount">
<span class="amount-value">{amount:.2f}</span>
<span class="amount-unit">THB</span>
</div>
<div class="result-range">
±{range_val:.2f} THB (MAE)
</div>
<div class="result-stats-grid">
<div class="stat-cell">
<div class="stat-value">{metrics['r2_score']*100:.1f}%</div>
<div class="stat-label">R² Score</div>
</div>
<div class="stat-cell">
<div class="stat-value">{breakdown['ac_cost']:.0f}฿</div>
<div class="stat-label">AC Cost</div>
</div>
<div class="stat-cell">
<div class="stat-value">{breakdown['appliances_cost']:.0f}฿</div>
<div class="stat-label">Appliances</div>
</div>
</div>
<div class="result-expand-cta">
<span>กดเพื่อดูผลลัพธ์เชิงลึก (Double Click on Card or Check Below)</span>
<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
<path d="M4 6L8 10L12 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
</div>
</div>""", unsafe_allow_html=True)
    
    # Always show detailed view if expanded is True passed from parent, 
    # but currently we just render it below since state management for expand/collapse 
    # inside component might be tricky without callbacks.
    # The prompt implies we might want to toggle it, but let's just render it for now.
    
    # Actually, let's put it in an expander for better UX if the user wants to toggle
    with st.expander("Show Detailed Analysis", expanded=expanded):
        render_detailed_analysis({
            'breakdown': breakdown,
            'model_metrics': metrics
        })

def render_detailed_analysis(prediction_data: dict):
    """Render detailed analysis view with animated charts"""
    
    breakdown = prediction_data['breakdown']
    metrics = prediction_data['model_metrics']
    
    st.markdown("---")
    st.markdown("### 📊 รายละเอียดการวิเคราะห์")
    
    # Model Performance Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
<div class="metric-box fade-in">
    <div class="metric-box-value">{metrics['r2_score']*100:.2f}%</div>
    <div class="metric-box-label">R² Score</div>
    <div class="metric-box-desc">Model Accuracy</div>
</div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
<div class="metric-box fade-in" style="animation-delay: 0.1s;">
    <div class="metric-box-value">{metrics['mae']:.2f}฿</div>
    <div class="metric-box-label">MAE</div>
    <div class="metric-box-desc">Mean Absolute Error</div>
</div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
<div class="metric-box fade-in" style="animation-delay: 0.2s;">
    <div class="metric-box-value">{metrics['rmse']:.2f}฿</div>
    <div class="metric-box-label">RMSE</div>
    <div class="metric-box-desc">Root Mean Squared Error</div>
</div>
        """, unsafe_allow_html=True)
    
    # Inject metric box styles (Non-f-string)
    st.markdown("""
    <style>
    .metric-box {
        background-color: var(--color-bg-surface);
        border: 1px solid var(--color-border);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    
    .metric-box-value {
        font-family: var(--font-mono);
        font-size: 32px;
        font-weight: 700;
        color: var(--color-accent-blue);
        margin-bottom: 8px;
    }
    
    .metric-box-label {
        font-size: 14px;
        font-weight: 600;
        color: var(--color-text-primary);
        margin-bottom: 4px;
    }
    
    .metric-box-desc {
        font-size: 12px;
        color: var(--color-text-muted);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Cost Breakdown Chart
    st.markdown("#### 💰 การแบ่งค่าใช้จ่าย")
    
    fig = create_cost_breakdown_chart(breakdown)
    st.plotly_chart(fig, use_container_width=True)

    # Export Report
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col2:
        try:
            pdf_data = create_pdf_report(prediction_data)
            st.download_button(
                label="📄 ดาวน์โหลดรายงาน (PDF)",
                data=pdf_data,
                file_name=f"roo-lot-report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"ไม่สามารถสร้างรายงานได้: {e}")

def create_cost_breakdown_chart(breakdown: dict) -> go.Figure:
    """Create animated cost breakdown bar chart"""
    
    categories = ['แอร์', 'เครื่องใช้ไฟฟ้า', 'ค่าพื้นฐาน']
    values = [
        breakdown['ac_cost'],
        breakdown['appliances_cost'],
        breakdown['base_fee']
    ]
    colors = ['#3b82f6', '#10b981', '#8b5cf6']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker=dict(
            color=colors,
            line=dict(color='#262626', width=1)
        ),
        text=[f'{v:.0f} THB' for v in values],
        textposition='outside',
        textfont=dict(
            family='JetBrains Mono',
            size=14,
            color='#ededed'
        )
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#ededed'),
        margin=dict(l=0, r=0, t=20, b=0),
        height=300,
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            tickfont=dict(size=13)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#262626',
            showline=False,
            zeroline=False,
            tickfont=dict(family='JetBrains Mono', size=12)
        ),
        transition={
            'duration': 500,
            'easing': 'cubic-in-out'
        }
    )
    
    return fig
