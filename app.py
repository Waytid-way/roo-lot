"""
Roo-Lot: Next Month Electricity Bill Predictor
Version: 2.1.0 - Bilingual Multi-Theme Edition

A machine learning powered web application to predict monthly electricity bills
with support for Thai and English languages and three beautiful themes.
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import datetime
import time
import plotly.graph_objects as go
from typing import Optional, Dict, Any
from contextlib import contextmanager

# Import theme and language manager
from utils.theme_manager import ThemeManager

# ===== Performance Monitoring =====
@contextmanager
def track_time(operation_name: str):
    """Track and display operation time for debugging"""
    start = time.time()
    yield
    duration = time.time() - start
    
    if duration > 1.0:  # Only show if operation takes > 1 second
        st.caption(f"Debug: {operation_name} took {duration:.2f}s")


# ===== Configuration =====
st.set_page_config(
    page_title="Roo-Lot: Electricity Bill Predictor",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Apply theme system
ThemeManager.apply_custom_css()

# Get current language
lang = ThemeManager.get_current_language()
t = ThemeManager.load_language(lang)  # t = translations


# ===== Model Loading =====
@st.cache_resource
def load_model() -> Optional[Any]:
    """
    Load the trained prediction model with error handling
    
    Returns:
        Trained model or None if loading fails
    """
    try:
        model = joblib.load('models/model_v2_next_month.pkl')
        return model
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"{t['error_unexpected']}: {str(e)}")
        return None


# ===== Validation Functions =====
def validate_unit_input(current: int, previous: int) -> tuple[bool, str]:
    """
    Validate electricity unit inputs for reasonable ranges
    
    Args:
        current: Current month's electricity usage (units)
        previous: Previous month's electricity usage (units)
        
    Returns:
        Tuple of (is_valid, message)
    """
    # Check reasonable range (typical household: 50-1000 units/month)
    if current < 0 or current > 2000:
        return False, "Current unit should be between 0-2000 kWh"
    
    if previous < 0 or previous > 2000:
        return False, "Previous unit should be between 0-2000 kWh"
    
    # Check for extreme changes (>300% increase or decrease)
    if previous > 0:
        change_pct = abs(current - previous) / previous
        if change_pct > 3.0:
            return False, f"Unusual change detected ({change_pct*100:.0f}%). Please verify your inputs."
    
    return True, "Valid"


class PredictionError(Exception):
    """Custom exception for prediction errors"""
    pass


def predict_with_error_handling(model: Any, input_data: pd.DataFrame) -> float:
    """
    Make prediction with comprehensive error handling
    
    Args:
        model: Trained prediction model
        input_data: Input features as DataFrame
        
    Returns:
        Predicted bill amount in THB
        
    Raises:
        PredictionError: If prediction fails or returns invalid value
    """
    try:
        prediction = model.predict(input_data)[0]
        
        # Sanity checks
        if np.isnan(prediction) or np.isinf(prediction):
            raise PredictionError("Model returned invalid numerical value (NaN or Inf)")
        
        if prediction < 0:
            raise PredictionError("Model predicted negative bill (model calibration issue)")
        
        if prediction > 50000:
            raise PredictionError("Unreasonably high bill predicted. Please check your inputs.")
        
        return max(0, prediction)
        
    except PredictionError:
        raise
    except Exception as e:
        raise PredictionError(f"Unexpected prediction error: {str(e)}")


# ===== History Management =====
def save_prediction_history(inputs: Dict[str, Any], prediction: float) -> None:
    """Save prediction to session history"""
    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []
    
    entry = {
        'timestamp': datetime.datetime.now(),
        'inputs': inputs,
        'prediction': prediction
    }
    
    st.session_state.prediction_history.append(entry)
    
    # Keep last 10 predictions only
    if len(st.session_state.prediction_history) > 10:
        st.session_state.prediction_history.pop(0)


def show_prediction_history() -> None:
    """Display recent predictions in sidebar"""
    if 'prediction_history' in st.session_state and st.session_state.prediction_history:
        st.sidebar.markdown(f"### {t['recent_predictions']}")
        
        history_df = pd.DataFrame([
            {
                t['time']: entry['timestamp'].strftime('%H:%M'),
                t['units']: entry['inputs']['current_unit'],
                t['bill']: f"{entry['prediction']:.0f} {t['baht']}"
            }
            for entry in reversed(st.session_state.prediction_history[-5:])
        ])
        
        st.sidebar.dataframe(
            history_df,
            hide_index=True,
            use_container_width=True
        )


def create_export_data(inputs: Dict[str, Any], prediction: float) -> pd.DataFrame:
    """Create exportable dataframe for CSV download"""
    return pd.DataFrame({
        'Prediction Date': [datetime.datetime.now().strftime('%Y-%m-%d %H:%M')],
        'Target Month': [datetime.date(2024, inputs['month'], 1).strftime('%B')],
        f"Current Unit ({t['units']})": [inputs['current_unit']],
        f"Previous Unit ({t['units']})": [inputs['lag1_unit']],
        f"Number of {t['people']}": [inputs['people']],
        'School Break': [t['break_yes'] if inputs['is_break'] else t['break_no']],
        f"Predicted Bill ({t['baht']})": [f"{prediction:.2f}"]
    })


# ===== Gauge Chart Creation =====
def create_gauge_chart(prediction: float) -> go.Figure:
    """
    Create a beautiful gauge chart for bill visualization
    
    Args:
        prediction: Predicted bill amount
        
    Returns:
        Plotly Figure object
    """
    # Get current theme colors
    palette = ThemeManager.get_color_palette()
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prediction,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={
            'suffix': f" {t['baht']}",
            'font': {'size': 32, 'color': palette['text']}
        },
        gauge={
            'axis': {
                'range': [None, 2000],
                'tickwidth': 1,
                'tickcolor': palette['text']
            },
            'bar': {'color': palette['primary']},
            'bgcolor': palette['secondary_bg'],
            'borderwidth': 2,
            'bordercolor': palette['text'],
            'steps': [
                {'range': [0, 500], 'color': palette['secondary_bg'], 'name': t['gauge_low']},
                {'range': [500, 1000], 'color': palette['background'], 'name': t['gauge_medium']},
                {'range': [1000, 2000], 'color': palette['secondary_bg'], 'name': t['gauge_high']}
            ],
            'threshold': {
                'line': {'color': palette['primary'], 'width': 4},
                'thickness': 0.75,
                'value': prediction
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor=palette['background'],
        plot_bgcolor=palette['background'],
        font={'color': palette['text'], 'family': "Inter, sans-serif"},
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig


# ===== Main Application =====
def main():
    """Main application entry point"""
    
    # Language toggle at top
    ThemeManager.render_language_toggle()
    
    # Header
    st.title(t['app_title'])
    st.markdown(f"### {t['tagline']}")
    st.caption(t['subtitle'])
    st.markdown("---")
    
    # Show prediction history (Modern st.data_editor)
    if 'prediction_history' in st.session_state and st.session_state.prediction_history:
        st.sidebar.markdown(f"### {t['recent_predictions']}")
        
        history_df = pd.DataFrame([
            {
                t['time']: entry['timestamp'].strftime('%H:%M'),
                t['units']: entry['inputs']['current_unit'],
                t['bill']: f"{entry['prediction']:.0f} {t['baht']}"
            }
            for entry in reversed(st.session_state.prediction_history[-5:])
        ])
        
        st.sidebar.data_editor(
            history_df,
            hide_index=True,
            use_container_width=True,
            disabled=True
        )
    
    # Sidebar - How to use
    with st.sidebar:
        st.markdown(f"### {t['how_to_use']}")
        st.markdown(f"""
        {t['step1']}  
        {t['step2']}  
        {t['step3']}  
        {t['step4']}
        """)
    
    # Load model with progress indicator
    with st.spinner("Loading Model..."):
        with track_time("Model Loading"):
            model = load_model()
    
    if model is None:
        st.error(f"⚠️ {t['error_model_not_found']}")
        st.info(f"{t['error_model_info']}: `python scripts/retrain_v2.py`")
        st.stop()
    
    # Input Form (Modern container style)
    with st.container(border=True):
        with st.form("prediction_form"):
            st.subheader(t['usage_details'])
            st.caption(t['usage_details_caption'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                current_unit = st.number_input(
                    t['current_unit'],
                    min_value=0,
                    max_value=2000,
                    value=100,
                    help=t['current_unit_help']
                )
                
                people = st.number_input(
                    t['people_count'],
                    min_value=1,
                    max_value=10,
                    value=2,
                    help=t['people_count_help']
                )
            
            with col2:
                lag1_unit = st.number_input(
                    t['previous_unit'],
                    min_value=0,
                    max_value=2000,
                    value=100,
                    help=t['previous_unit_help']
                )
                
                # Month Selection (Default to next month)
                today = datetime.date.today()
                if today.month == 12:
                    default_month_idx = 0  # January
                else:
                    default_month_idx = today.month  # Next month index (0-11)
                
                month = st.selectbox(
                    t['target_month'],
                    options=list(range(1, 13)),
                    index=default_month_idx,
                    format_func=lambda x: datetime.date(2024, x, 1).strftime('%B'),
                    help=t['target_month_help']
                )
            
            # Modern Toggle for School Break
            is_break_input = st.toggle(
                t['is_break'],
                value=False,
                help=t['is_break_help']
            )
            is_break = 1 if is_break_input else 0
            
            st.markdown("")  # Spacing
            submit = st.form_submit_button(
                t['predict_button'],
                use_container_width=True,
                type="primary"
            )
    
    # Process prediction
    if submit:
        # Validate inputs
        is_valid, validation_msg = validate_unit_input(current_unit, lag1_unit)
        
        if not is_valid:
            st.warning(f"{t['validation_warning']}: {validation_msg}")
            st.info(t['validation_info'])
        
        # Prepare input data
        input_data = pd.DataFrame({
            'current_unit': [current_unit],
            'is_break': [is_break],
            'month': [month],
            'people': [people],
            'lag1_unit': [lag1_unit]
        })
        
        # Make prediction with error handling
        try:
            with st.spinner("Calculating Prediction..."):
                with track_time("Prediction"):
                    prediction = predict_with_error_handling(model, input_data)
            
            # Use Toast for transient success message
            st.toast("Prediction Calculated Successfully!", icon="✅")
            
            # Store prediction for export
            prediction_inputs = {
                'current_unit': current_unit,
                'lag1_unit': lag1_unit,
                'people': people,
                'month': month,
                'is_break': is_break
            }
            
            # Save to history
            save_prediction_history(prediction_inputs, prediction)
            
            # Store in session state for export
            st.session_state.last_prediction = prediction
            st.session_state.last_prediction_inputs = prediction_inputs
            
            # Display results
            st.markdown("---")
            st.markdown(f"## {t['predicted_bill']}")
            
            # Two columns: Amount + Gauge
            col_result1, col_result2 = st.columns([0.5, 0.5])
            
            with col_result1:
                st.markdown(f"### {t['predicted_bill_subtitle']}")
                st.markdown(f"# **{prediction:,.0f}** {t['baht']}")
                
                # Additional metrics
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.metric(
                        t['input_units'],
                        f"{current_unit} {t['units']}"
                    )
                
                with col_b:
                    if lag1_unit > 0:
                        change = ((current_unit - lag1_unit) / lag1_unit) * 100
                        st.metric(
                            t['usage_change'],
                            f"{abs(change):.1f}%",
                            delta=f"{change:+.1f}%"
                        )
                    else:
                        st.metric(t['usage_change'], "N/A")
                
                # Rate per unit
                rate_per_unit = prediction / max(current_unit, 1)
                st.metric(
                    t['rate_per_unit'],
                    f"{rate_per_unit:.2f} {t['baht']}"
                )
            
            with col_result2:
                # Gauge Chart
                fig = create_gauge_chart(prediction)
                st.plotly_chart(fig, use_container_width=True)
            
            # Usage category feedback
            if current_unit < 100:
                usage_category = t['usage_low']
                usage_icon = t['efficient_user']
            elif current_unit < 300:
                usage_category = t['usage_moderate']
                usage_icon = t['normal_user']
            else:
                usage_category = t['usage_high']
                usage_icon = t['heavy_user']
            
            st.info(f"{t['usage_category']}: **{usage_category}** ({usage_icon})")
            
            # Contextual insights
            if is_break:
                st.info(f"{t['note']}: {t['break_note']}")
            
            # Export functionality
            st.markdown("---")
            export_df = create_export_data(prediction_inputs, prediction)
            csv = export_df.to_csv(index=False)
            
            col_export1, col_export2 = st.columns([2, 1])
            
            with col_export1:
                st.download_button(
                    label=t['download_csv'],
                    data=csv,
                    file_name=f"roolot_prediction_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_export2:
                if st.button(t['clear_history'], use_container_width=True):
                    st.session_state.prediction_history = []
                    st.rerun()
            
            # Disclaimer
            st.caption(f"⚠️ {t['disclaimer']}")
            
        except PredictionError as e:
            st.error(f"{t['error_prediction']}: {str(e)}")
            st.info("Please verify your inputs or contact support if the issue persists.")
            
            with st.expander("Technical Details"):
                st.code(str(e))
                st.write("Input Data:", input_data)
                
        except Exception as e:
            st.error(t['error_unexpected'])
            
            with st.expander("Technical Details for Debugging"):
                st.code(str(e))
                st.write("Input Data:", input_data)
    
    # Footer
    st.markdown("---")
    current_theme = ThemeManager.get_current_theme()
    current_lang = ThemeManager.get_current_language()
    st.caption(
        f"{t['footer']} | "
        f"{t['version']}: 2.1.0 | "
        f"{t['model']}: Ridge Regression | "
        f"{t['theme']}: {current_theme.title()} | "
        f"Lang: {current_lang.upper()}"
    )


# ===== Application Entry Point =====
if __name__ == "__main__":
    main()
