# tests/test_components.py
import pytest
from components.chat_message import render_message
from components.result_card import render_result_card
import streamlit as st
import pandas as pd

class TestUIComponents:
    """Test UI rendering and edge cases"""
    
    # We can mock st.markdown to verify it's called, rather than relying on AppTest for unit tests
    # AppTest is better for integration
    
    def test_render_message_user(self, mocker):
        """Test: User message renders without error"""
        mock_markdown = mocker.patch('streamlit.markdown')
        
        try:
            render_message(
                role="user",
                content="ผมใช้แอร์ 5 ชั่วโมงต่อวัน",
                timestamp="14:30"
            )
            success = True
        except Exception as e:
            success = False
            pytest.fail(f"render_message failed: {e}")
        
        assert success
        # Check if markdown was called (it might be called multiple times for style and content)
        assert mock_markdown.called
    
    def test_render_message_assistant(self, mocker):
        """Test: Assistant message renders without error"""
        mocker.patch('streamlit.markdown')
        try:
            render_message(
                role="assistant",
                content="คุณใช้แอร์กี่ชั่วโมงต่อวันครับ?",
                timestamp="14:29"
            )
            success = True
        except Exception:
            success = False
        
        assert success
    
    def test_result_card_with_valid_data(self, mocker):
        """Test: Result card displays prediction correctly"""
        mocker.patch('streamlit.markdown')
        mocker.patch('streamlit.expander') # Mock expander context
        mocker.patch('components.result_card.render_detailed_analysis')
        
        # Mock create_pdf_report to avoid PDF generation errors during test if it's called
        mocker.patch('components.result_card.create_pdf_report')
        
        valid_prediction = {
            'amount': 1500.50,
            'range': 75.0,
            'breakdown': {
                'ac_cost': 800,
                'appliances_cost': 500,
                'base_fee': 200.50
            },
            'model_metrics': {
                'r2_score': 0.99,
                'mae': 40.0,
                'rmse': 50.0
            }
        }
        
        try:
            render_result_card(valid_prediction, expanded=False)
            success = True
        except Exception as e:
            success = False
            pytest.fail(f"Result card render failed: {e}")
        
        assert success
    
    def test_result_card_missing_breakdown(self, mocker):
        """Test: Result card handles missing breakdown gracefully"""
        mocker.patch('streamlit.markdown')
        mocker.patch('streamlit.expander')
        mocker.patch('components.result_card.render_detailed_analysis')
        
        incomplete_prediction = {
            'amount': 1500,
            'range': 75.0
            # Missing 'breakdown'
        }
        
        # Should not crash because component has fullback logic?
        # Let's check the code: yes, .get('breakdown', defaults)
        try:
            render_result_card(incomplete_prediction, expanded=False)
        except KeyError as e:
            pytest.fail(f"Result card failed on missing breakdown: {e}")
