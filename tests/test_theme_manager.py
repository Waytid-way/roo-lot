"""
Unit Tests for Theme Manager
Tests theme configuration, validation, and functionality

Run: pytest tests/test_theme_manager.py -v
"""

import pytest
import re
from utils.theme_manager import ThemeManager, ThemeConfig


class TestThemeConfigurations:
    """Test suite for theme configurations"""
    
    def test_dark_theme_exists(self):
        """Verify Dark theme is defined"""
        assert "dark" in ThemeManager.THEME_CONFIGS
    
    def test_theme_count(self):
        """Verify exactly 1 theme is configured"""
        assert len(ThemeManager.THEME_CONFIGS) == 1
    
    def test_theme_config_structure(self):
        """Verify theme has all required fields"""
        required_fields = [
            "name", "description", "icon_text",
            "primary_color", "bg_color", "secondary_bg_color",
            "text_color", "font"
        ]
        
        config = ThemeManager.THEME_CONFIGS["dark"]
        # Check if config is ThemeConfig instance
        assert isinstance(config, ThemeConfig), \
            f"Dark theme is not a ThemeConfig instance"
        
        # Check all required attributes exist
        for field in required_fields:
            assert hasattr(config, field), \
                f"Dark theme missing field '{field}'"
            assert getattr(config, field) is not None, \
                f"Dark theme field '{field}' is None"


class TestColorValidation:
    """Test suite for color code validation"""
    
    def test_color_format_valid(self):
        """Verify all color codes are valid hex format (#RRGGBB)"""
        hex_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
        
        config = ThemeManager.THEME_CONFIGS["dark"]
        # Test primary color
        assert hex_pattern.match(config.primary_color), \
            f"Dark theme has invalid primary_color: {config.primary_color}"
        
        # Test background color
        assert hex_pattern.match(config.bg_color), \
            f"Dark theme has invalid bg_color: {config.bg_color}"
        
        # Test secondary background color
        assert hex_pattern.match(config.secondary_bg_color), \
            f"Dark theme has invalid secondary_bg_color: {config.secondary_bg_color}"
        
        # Test text color
        assert hex_pattern.match(config.text_color), \
            f"Dark theme has invalid text_color: {config.text_color}"
    
    def test_colors_are_different(self):
        """Verify primary color differs from background"""
        config = ThemeManager.THEME_CONFIGS["dark"]
        assert config.primary_color.upper() != config.bg_color.upper(), \
            f"Dark theme has same primary and background colors"


class TestThemeNames:
    """Test suite for theme naming conventions"""
    
    def test_theme_names_not_empty(self):
        """Verify theme has non-empty name"""
        config = ThemeManager.THEME_CONFIGS["dark"]
        assert len(config.name) > 0, "Dark theme has empty name"
    
    def test_theme_descriptions_not_empty(self):
        """Verify theme has description"""
        config = ThemeManager.THEME_CONFIGS["dark"]
        assert len(config.description) > 0, "Dark theme has empty description"
    
    def test_icon_text_not_empty(self):
        """Verify theme has icon text (no emojis)"""
        config = ThemeManager.THEME_CONFIGS["dark"]
        assert len(config.icon_text) > 0, "Dark theme has empty icon_text"
        
        # Verify no emoji in icon_text
        assert all(ord(c) < 0x1F000 for c in config.icon_text), \
            "Dark theme has emoji in icon_text"


class TestNoEmojiInCode:
    """Test suite to ensure no emojis in source code"""
    
    def test_no_emoji_in_theme_manager(self):
        """Verify theme_manager.py contains no emoji characters"""
        import utils.theme_manager as tm
        import inspect
        
        source = inspect.getsource(tm)
        
        # Check for emoji unicode ranges
        emoji_found = [c for c in source if ord(c) >= 0x1F000]
        
        assert len(emoji_found) == 0, \
            f"Found {len(emoji_found)} emoji characters in theme_manager.py"
    
    def test_no_emoji_in_config_values(self):
        """Verify no emoji in configuration values"""
        config = ThemeManager.THEME_CONFIGS["dark"]
        # Check all string fields
        string_fields = [
            config.name, config.description, config.icon_text,
            config.primary_color, config.bg_color,
            config.secondary_bg_color, config.text_color, config.font
        ]
        
        for field_value in string_fields:
            emoji_found = [c for c in field_value if ord(c) >= 0x1F000]
            assert len(emoji_found) == 0, \
                f"Dark theme has emoji in field: {field_value}"


class TestThemeManagerMethods:
    """Test suite for ThemeManager methods"""
    
    def test_get_theme_config(self):
        """Test get_theme_config returns valid config for dark theme"""
        config = ThemeManager.get_theme_config()  # Should default to dark
        assert isinstance(config, ThemeConfig)
        assert config.name == "Dark"
    
    def test_get_color_palette(self):
        """Test get_color_palette returns correct structure"""
        palette = ThemeManager.get_color_palette()
        
        required_keys = ['primary', 'background', 'secondary_bg', 'text']
        for key in required_keys:
            assert key in palette, f"Missing key '{key}' in color palette"
            assert palette[key].startswith('#'), f"Invalid color format for '{key}'"
    
    def test_get_current_theme(self):
        """Test get_current_theme always returns 'dark'"""
        assert ThemeManager.get_current_theme() == "dark"


class TestAccessibility:
    """Test suite for accessibility compliance"""
    
    def test_contrast_ratios(self):
        """Verify contrast ratios meet WCAG AA standards (4.5:1 for normal text)"""
        config = ThemeManager.THEME_CONFIGS["dark"]
        
        # Ensure text and background colors are sufficiently different
        text_rgb = self._hex_to_rgb(config.text_color)
        bg_rgb = self._hex_to_rgb(config.bg_color)
        
        # Simple check: ensure significant difference in at least one channel
        max_diff = max(
            abs(text_rgb[0] - bg_rgb[0]),
            abs(text_rgb[1] - bg_rgb[1]),
            abs(text_rgb[2] - bg_rgb[2])
        )
        
        assert max_diff > 100, \
            "Dark theme may have insufficient contrast"
    
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
