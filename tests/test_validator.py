# tests/test_validator.py
import pytest
from conversation.validator import InputValidator

class TestInputValidator:
    """Test input validation rules"""
    
    @pytest.fixture
    def validator(self):
        return InputValidator()
    
    def test_numeric_validation(self, validator):
        """Test: Numeric inputs are validated correctly"""
        question = {"min": 0, "max": 100, "unit": ""}
        
        # Valid cases
        valid, val, err = validator.validate("50", question)
        assert valid
        assert val == 50.0
        assert err is None
        
        valid, val, err = validator.validate("10.5", question)
        assert valid
        assert val == 10.5
        
        # Invalid cases
        valid, val, err = validator.validate("abc", question)
        assert not valid
        assert "ตัวเลข" in err
        
    def test_range_validation(self, validator):
        """Test: Range constraints work properly"""
        question = {"min": 10, "max": 20, "unit": ""}
        
        # Valid
        valid, val, err = validator.validate("15", question)
        assert valid
        
        # Too low
        valid, val, err = validator.validate("5", question)
        assert not valid
        assert "ระหว่าง" in err
        
        # Too high
        valid, val, err = validator.validate("25", question)
        assert not valid
        assert "ระหว่าง" in err

    def test_special_validation_methods(self, validator):
        """Test specific validation methods if they exist"""
        # room_size validation
        assert validator.validate_room_size(50) == True
        assert validator.validate_room_size(5) == False
        
        # ac_hours validation
        assert validator.validate_ac_hours(12) == True
        assert validator.validate_ac_hours(25) == False
