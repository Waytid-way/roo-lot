"""
Roo-Lot Chatbot - Input Validator
"""

from typing import Tuple, Union, Optional

class InputValidator:
    """Validator for user inputs in the chatbot"""
    
    def validate(self, text: str, question: dict) -> Tuple[bool, Union[float, None], Optional[str]]:
        """
        Validate user input against question constraints
        
        Args:
            text: Raw input string
            question: Question dictionary containing validation rules
            
        Returns:
            Tuple of (is_valid, parsed_value, error_message)
        """
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
    
    def validate_room_size(self, val: float) -> bool:
        return 10 <= val <= 100
        
    def validate_ac_hours(self, val: float) -> bool:
        return 0 <= val <= 24
