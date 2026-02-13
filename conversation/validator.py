"""
Roo-Lot Chatbot - Input Validator
"""

from typing import Tuple, Union, Optional

class InputValidator:
    """Validator for user inputs in the chatbot"""
    
    def validate(self, text: str, question: dict) -> Tuple[bool, Union[float, str, None], Optional[str]]:
        """
        Validate user input against question constraints
        
        Args:
            text: Raw input string
            question: Question dictionary containing validation rules
            
        Returns:
            Tuple of (is_valid, parsed_value, error_message)
        """
        # Strip whitespace and convert to lowercase for flexible matching
        text_clean = text.strip()
        text_lower = text_clean.lower()
        
        q_type = question.get('type', 'number')

        # 1. Choice / Radio Type
        if q_type == 'choice':
            options = question.get('options', [])
            
            # Flexible matching - check exact match, case-insensitive match, or quick replies
            for option in options:
                if text_clean == option or text_lower == option.lower():
                    return True, option, None  # Return the standardized option value
            
            # Check if it matches quick replies
            quick_replies = question.get('quick_replies', [])
            for reply in quick_replies:
                if text_clean == reply or text_lower == reply.lower():
                    return True, reply, None
            
            # If no match found, show error
            return False, None, f"กรุณาเลือกหนึ่งในตัวเลือก: {', '.join(options)}"

        # 2. Month Selector Type
        if q_type == 'month_selector':
            # Basic check if it's a known month string or number 1-12
            # We let the predictor parse it strictly later, but here we check basic validity
            if text.isdigit():
                val = int(text)
                if 1 <= val <= 12:
                    return True, val, None
                else:
                    return False, None, "กรุณาส่งเดือนระหว่าง 1-12 ครับ"
            
            # If string (Thai month name), assume valid if length > 2
            if len(text) > 2: 
                return True, text, None
            
            return False, None, "กรุณาระบุเดือนให้ถูกต้องครับ"

        # 3. Numeric Type (Default)
        try:
            # Basic numeric check
            val = float(text)
            
            # Range check with custom logic per field if needed
            min_val = question.get('min', 0)
            max_val = question.get('max', float('inf'))
            unit = question.get('unit', '')
            
            if min_val <= val <= max_val:
                return True, val, None
            
            # Error message for out-of-range
            return False, None, f"กรุณากรอกตัวเลขระหว่าง {min_val} ถึง {max_val} {unit} ครับ"
            
        except ValueError:
            # Error message for non-numeric
            return False, None, "กรุณากรอกเฉพาะตัวเลขเท่านั้นครับ"
