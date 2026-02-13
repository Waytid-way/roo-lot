"""
Roo-Lot Chatbot - Conversation Manager
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import streamlit as st
import time
from .questions import QUESTIONS
from .validator import InputValidator

class ConversationManager:
    """Manages conversation flow and state"""
    
    def __init__(self):
        self.questions = QUESTIONS
        self.validator = InputValidator()
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state variables"""
        if 'conversation_stage' not in st.session_state:
            st.session_state.conversation_stage = 0  # 0=landing, 1-6=questions, 7=result
        
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        if 'user_inputs' not in st.session_state:
            st.session_state.user_inputs = {}
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        if 'current_prediction' not in st.session_state:
            st.session_state.current_prediction = None
        
        if 'show_detailed_results' not in st.session_state:
            st.session_state.show_detailed_results = False
        
        if 'is_processing' not in st.session_state:
            st.session_state.is_processing = False
        
        if 'is_typing' not in st.session_state:
            st.session_state.is_typing = False
    
    def start_conversation(self):
        """Start a new conversation"""
        st.session_state.conversation_stage = 1
        st.session_state.messages = []
        st.session_state.user_inputs = {}
        st.session_state.current_prediction = None
        st.session_state.show_detailed_results = False
        
        # Add first question
        first_q = self.get_current_question()
        if first_q:
            self.add_bot_message(first_q["question"])
    
    def reset_conversation(self):
        """Reset to start a new conversation"""
        # Save current conversation to history if prediction exists (Handled by app_chatbot generally, but safe to do here if needed?? No, let's stick to what we decided: remove double save)
        # Reset states
        st.session_state.conversation_stage = 1
        st.session_state.messages = []
        st.session_state.user_inputs = {}
        st.session_state.current_prediction = None
        st.session_state.show_detailed_results = False
        st.session_state.is_typing = False
        
        # Start fresh
        first_q = self.get_current_question()
        if first_q:
            self.add_bot_message(first_q["question"])
    
    def get_current_question(self) -> Optional[Dict]:
        """Get current question based on stage"""
        input_count = len(st.session_state.user_inputs)
        if input_count < len(self.questions):
            return self.questions[input_count]
        return None
    
    def add_bot_message(self, content: str):
        """Add a bot message to conversation"""
        message = {
            "role": "assistant", # Changed from 'bot' to 'assistant' to match app_chatbot.py
            "content": content,
            "timestamp": datetime.now().strftime("%H:%M")
        }
        st.session_state.messages.append(message)
    
    def add_user_message(self, content: str):
        """Add a user message to conversation"""
        message = {
            "role": "user",
            "content": content,
            "timestamp": datetime.now().strftime("%H:%M")
        }
        st.session_state.messages.append(message)
    
    def process_user_input(self, user_input: str) -> bool:
        """
        Process user input and advance conversation
        
        Returns:
            bool: True if input was valid and processed, False otherwise
        """
        current_q = self.get_current_question()
        if not current_q:
            return False
        
        # Add user message first (before validation) so user can see what they sent
        self.add_user_message(user_input)
        
        # Validate input using validator
        is_valid, parsed_value, error_msg = self.validator.validate(user_input, current_q)
        
        if not is_valid:
            self.add_bot_message(error_msg)
            return False
        
        # Store valid input
        field_name = current_q["id"] 
        st.session_state.user_inputs[field_name] = parsed_value
        
        # Check if conversation is complete
        if len(st.session_state.user_inputs) >= len(self.questions):
            st.session_state.conversation_stage = 2 # Result stage
            return True
        
        # Ask next question
        next_q = self.get_current_question()
        if next_q:
            self.add_bot_message(next_q["question"])
        
        return True

    def is_conversation_complete(self) -> bool:
        """Check if all questions have been answered"""
        return len(st.session_state.user_inputs) >= len(self.questions)
    
    def get_collected_inputs(self) -> Dict[str, float]:
        """Get all collected user inputs"""
        return st.session_state.user_inputs.copy()
    
    def save_to_history(self):
        """Save current conversation to history"""
        if not st.session_state.current_prediction:
            return
        
        history_item = {
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "inputs": st.session_state.user_inputs.copy(),
            "predicted_bill": st.session_state.current_prediction.get("amount", 0),
            # "messages": st.session_state.messages.copy() # Optional, maybe too heavy
        }
        
        if 'chat_history' not in st.session_state:
             st.session_state.chat_history = []

        st.session_state.chat_history.append(history_item)
        
        # Keep only last 10 conversations
        if len(st.session_state.chat_history) > 10:
            st.session_state.chat_history = st.session_state.chat_history[-10:]
    
    def load_from_history(self, history_index: int):
        """Load a conversation from history"""
        # history_index is likely index from reversed list in UI
        # We need actual index
        if 'chat_history' in st.session_state:
             if 0 <= history_index < len(st.session_state.chat_history):
                history_item = st.session_state.chat_history[history_index]
                
                # st.session_state.messages = history_item.get("messages", []).copy()
                st.session_state.messages = [] # Reset messages if not stored
                st.session_state.user_inputs = history_item["inputs"].copy()
                st.session_state.conversation_stage = 2  # Result stage
                st.session_state.current_prediction = None  # Will re-predict
                st.session_state.show_detailed_results = False
                
                return True
        return False
