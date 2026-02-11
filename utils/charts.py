"""
Chart Components for Roo-Lot v4
Modern gauges and visualizations using Plotly
Matches React SVG design aesthetic

Author: Roo-Lot Dev Team
Version: 4.0.0
"""

import plotly.graph_objects as go
from typing import Optional, Dict


def create_modern_gauge(
    value: Optional[float],
    theme_colors: Dict[str, str],
    min_value: float = 0,
    max_value: float = 2000,
    unit: str = "Units",
    lang: str = 'th'
) -> go.Figure:
    """
    Create a modern semicircle gauge chart matching React design
    
    Args:
        value: The value to display (None for empty state)
        theme_colors: Dictionary of theme colors from theme_system
        min_value: Minimum gauge value
        max_value: Maximum gauge value
        unit: Unit label
        lang: Language code
        
    Returns:
        Plotly Figure object
    """
    
    display_value = value if value is not None else 0
    
    # Color thresholds
    if display_value < 500:
        bar_color = theme_colors.get('success', '#10b981')
        status_text = 'Low' if lang == 'en' else 'ต่ำ'
    elif display_value < 1000:
        bar_color = theme_colors.get('warning', '#f59e0b')
        status_text = 'Moderate' if lang == 'en' else 'ปานกลาง'
    else:
        bar_color = theme_colors.get('error', '#ef4444')
        status_text = 'High' if lang == 'en' else 'สูง'
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=display_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={
            'suffix': f" {unit}",
            'font': {
                'size': 0,  # Hide the built-in number, we'll show it separately
                'color': theme_colors.get('text_heading', '#ffffff'),
                'family': 'Inter, sans-serif'
            }
        },
        gauge={
            'axis': {
                'range': [min_value, max_value],
                'tickwidth': 1,
                'tickcolor': theme_colors.get('text_muted', '#707070'),
                'tickfont': {
                    'color': theme_colors.get('text_muted', '#A0A0A0'),
                    'size': 10
                },
                'showticklabels': True
            },
            'bar': {
                'color': bar_color,
                'thickness': 0.7
            },
            'bgcolor': theme_colors.get('bg_primary', '#0a0a0a'),
            'borderwidth': 0,
            'steps': [
                {
                    'range': [0, 500],
                    'color': theme_colors.get('gauge_base', '#333'),
                    'thickness': 0.7
                },
                {
                    'range': [500, 1000],
                    'color': theme_colors.get('gauge_base', '#333'),
                    'thickness': 0.7
                },
                {
                    'range': [1000, max_value],
                    'color': theme_colors.get('gauge_base', '#333'),
                    'thickness': 0.7
                }
            ],
            'threshold': {
                'line': {
                    'color': bar_color,
                    'width': 3
                },
                'thickness': 0.8,
                'value': display_value
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor=theme_colors.get('bg_card', '#121212'),
        plot_bgcolor=theme_colors.get('bg_card', '#121212'),
        font={
            'color': theme_colors.get('text_primary', '#FFFFFF'),
            'family': 'Inter, sans-serif'
        },
        height=280,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False
    )
    
    return fig


def create_simple_arc_gauge(
    value: Optional[float],
    theme_colors: Dict[str, str],
    max_value: float = 2000
) -> str:
    """
    Create a pure SVG arc gauge for cleaner look (alternative to Plotly)
    Returns HTML string with embedded SVG
    
    Args:
        value: The value to display
        theme_colors: Dictionary of theme colors
        max_value: Maximum value
        
    Returns:
        HTML string with SVG gauge
    """
    
    display_value = value if value is not None else 0
    percentage = min(display_value / max_value, 1.0)
    
    # Arc calculations
    radius = 80
    stroke_width = 12
    circumference = radius * 3.14159  # Half circle
    stroke_dashoffset = circumference - (percentage * circumference)
    
    # Determine color based on value
    if display_value < 500:
        fill_color = theme_colors.get('success', '#10b981')
    elif display_value < 1000:
        fill_color = theme_colors.get('warning', '#f59e0b')
    else:
        fill_color = theme_colors.get('gauge_fill', '#06b6d4')
    
    svg_html = f"""
    <div style="display: flex; justify-content: center; align-items: center; padding: 20px;">
        <svg width="200" height="120" viewBox="0 0 200 120" style="overflow: visible;">
            <!-- Background Arc -->
            <path
                d="M 20 100 A 80 80 0 0 1 180 100"
                fill="none"
                stroke="{theme_colors.get('gauge_base', '#333')}"
                stroke-width="{stroke_width}"
                stroke-linecap="round"
            />
            <!-- Fill Arc -->
            <path
                d="M 20 100 A 80 80 0 0 1 180 100"
                fill="none"
                stroke="{fill_color}"
                stroke-width="{stroke_width}"
                stroke-linecap="round"
                stroke-dasharray="{circumference}"
                stroke-dashoffset="{stroke_dashoffset}"
                style="transition: stroke-dashoffset 1s ease-out;"
            />
        </svg>
    </div>
    """
    
    return svg_html


def create_mini_sparkline(
    values: list,
    theme_colors: Dict[str, str],
    width: int = 100,
    height: int = 30
) -> go.Figure:
    """
    Create a minimal sparkline chart for history trends
    
    Args:
        values: List of values to plot
        theme_colors: Dictionary of theme colors
        width: Chart width
        height: Chart height
        
    Returns:
        Plotly Figure object
    """
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        y=values,
        mode='lines',
        line=dict(
            color=theme_colors.get('accent_primary', '#06b6d4'),
            width=2
        ),
        fill='tozeroy',
        fillcolor=theme_colors.get('accent_muted', 'rgba(6, 182, 212, 0.1)'),
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=height,
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False
        )
    )
    
    return fig


def create_status_indicator(
    value: float,
    lang: str = 'th'
) -> tuple[str, str]:
    """
    Determine status and color based on value
    
    Args:
        value: The prediction value
        lang: Language code
        
    Returns:
        Tuple of (status_text, status_class)
    """
    
    if value < 500:
        status_text = 'Low' if lang == 'en' else 'ต่ำ'
        status_class = 'success'
    elif value < 1000:
        status_text = 'Moderate' if lang == 'en' else 'ปานกลาง'
        status_class = 'warning'
    else:
        status_text = 'High' if lang == 'en' else 'สูง'
        status_class = 'error'
    
    return status_text, status_class
