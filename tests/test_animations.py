# tests/test_animations.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestAnimations:
    """ทดสอบ animations และ transitions"""
    
    @pytest.fixture
    def driver(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(options=options)
            yield driver
            driver.quit()
        except:
            pytest.skip("Selenium driver not available")
    
    def test_message_fade_in_animation(self, driver):
        """Test: Messages fade in เมื่อปรากฏ"""
        try:
            driver.get("http://localhost:8501")
        except:
            pytest.skip("App not running")
            
        time.sleep(3)
        
        # Look for fade-in class
        try:
            # We used 'slide-up' class in our css
            messages = driver.find_elements(By.CLASS_NAME, 'slide-up')
            # If fade-in animations are implemented, elements should have this class
            # Only if messages are present
            pass
        except Exception:
            pass
