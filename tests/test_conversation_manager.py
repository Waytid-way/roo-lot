# tests/test_conversation_manager.py
import pytest
from conversation.manager import ConversationManager
import streamlit as st
from datetime import datetime

class TestConversationManager:
    """Test suite for conversation flow and state management"""
    
    @pytest.fixture
    def setup_session_state(self, mocker):
        """Mock Streamlit session state"""
        # Create a real dict to hold state
        state = {
            'conversation_stage': 0,
            'messages': [],
            'user_inputs': {},
            'chat_history': [],
            'current_prediction': None,
            'show_detailed_results': False,
            'is_processing': False,
            'is_typing': False
        }
        
        # Mock st.session_state to behave like an object backed by this dict
        # We need it to support both attribute access (.x) and item access (['x'])
        
        class SessionState(dict):
            def __getattr__(self, key):
                if key in self:
                    return self[key]
                raise AttributeError(f"SessionState has no attribute '{key}'")
            
            def __setattr__(self, key, value):
                self[key] = value
                
        mock_state = SessionState(state)
        mocker.patch('streamlit.session_state', mock_state)
        yield mock_state
    
    @pytest.fixture
    def manager(self, setup_session_state):
        return ConversationManager()
    
    def test_initialization(self, manager):
        """Test: Manager initializes correctly"""
        assert manager is not None
        assert hasattr(manager, 'start_conversation')
        assert hasattr(manager, 'process_user_input')
        assert st.session_state.conversation_stage == 0
    
    def test_start_conversation(self, manager):
        """Test: Conversation starts and moves to stage 1"""
        manager.start_conversation()
        assert st.session_state.conversation_stage == 1
        assert len(st.session_state.messages) > 0
        assert st.session_state.messages[0]['role'] == 'assistant'
    
    def test_process_valid_input(self, manager):
        """Test: Valid input is processed correctly"""
        manager.start_conversation()
        current_q = manager.get_current_question()
        
        if current_q:
            # First question is room_size (min 10)
            test_input = "30" 
            manager.process_user_input(test_input)
            
            # Check if input was saved
            assert len(st.session_state.user_inputs) > 0
            # Check if conversation progressed (bot asks next question)
            assert len(st.session_state.messages) >= 2 
    
    def test_invalid_input_handling(self, manager):
        """Test: Invalid inputs are rejected with proper error messages"""
        manager.start_conversation()
        
        invalid_inputs = [
            "abc",        # Non-numeric
            "-5",         # Negative number
            "999",        # Out of range (usually)
        ]
        
        for invalid_input in invalid_inputs:
            initial_count = len(st.session_state.messages)
            manager.process_user_input(invalid_input)
            
            # Should add error message from bot
            assert len(st.session_state.messages) > initial_count
            last_message = st.session_state.messages[-1]
            assert last_message['role'] == 'assistant'
            # Validator error messages usually contain "กรุณา"
            assert 'กรุณา' in last_message.get('content', '')

    def test_conversation_completion(self, manager):
        """Test: Conversation completes after all questions answered"""
        manager.start_conversation()
        
        # Simulate answering all questions based on QUESTIONS structure
        # Add safety counter to prevent infinite loop
        max_iterations = 20
        iterations = 0
        
        while not manager.is_conversation_complete() and iterations < max_iterations:
            current_q = manager.get_current_question()
            if not current_q:
                break
                
            # Provide valid dummy answer based on question type/id
            qid = current_q.get('id', '')
            answer = "2" # Safe default for small numeric fields (fans, lights, etc.)
            
            if 'room' in qid: answer = "30" # min 10
            if 'ac' in qid: answer = "8" # max 24
            if 'people' in qid: answer = "2" # usually safe
            if 'computers' in qid: answer = "1" # max 5
            
            manager.process_user_input(answer)
            iterations += 1
        
        assert manager.is_conversation_complete()
        assert st.session_state.conversation_stage == 2 # Result stage

    def test_reset_conversation(self, manager):
        """Test: Reset clears all state correctly"""
        manager.start_conversation()
        manager.process_user_input("5")
        
        manager.reset_conversation()
        
        # Should be back to start (stage 1 per implementation, not 0)
        # Check manager.reset_conversation implementation: it sets stage to 1 and starts fresh
        assert st.session_state.conversation_stage == 1 
        assert len(st.session_state.user_inputs) == 0
        assert len(st.session_state.messages) > 0 # First question asked again

    def test_get_collected_inputs(self, manager):
        """Test: Collected inputs format is correct"""
        manager.start_conversation()
        
        st.session_state.user_inputs = {"ac_hours": 5, "room_size": 30}
        collected = manager.get_collected_inputs()
        
        assert isinstance(collected, dict)
        assert collected['ac_hours'] == 5
        assert collected['room_size'] == 30
