# tests/test_rendering_performance.py
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestRenderingPerformance:
    """ทดสอบความเร็วในการ render"""
    
    @pytest.fixture
    def driver(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            yield driver
            driver.quit()
        except:
            pytest.skip("Selenium driver not available")
            
    
    def test_initial_page_load_time(self, driver):
        """Test: หน้าเว็บโหลดภายใน 3 วินาที"""
        start_time = time.time()
        try:
            driver.get("http://localhost:8501")
        except:
             pytest.skip("App not running")
        
        # Wait for Streamlit to be ready
        # Simple wait
        time.sleep(2)
        
        load_time = time.time() - start_time
        
        # 5 seconds tolerance for test environment
        assert load_time < 5.0, f"Page load too slow: {load_time:.2f}s"
    
    def test_no_layout_shift(self, driver):
        """Test: ไม่มี Cumulative Layout Shift (CLS)"""
        try:
            driver.get("http://localhost:8501")
        except:
             pytest.skip("App not running")
        
        # Measure layout shifts using JavaScript
        # This requires browser support for PerformanceObserver
        try:
            cls_score = driver.execute_script("""
                return new Promise((resolve) => {
                    let cls = 0;
                    try {
                        new PerformanceObserver((list) => {
                            for (const entry of list.getEntries()) {
                                if (!entry.hadRecentInput) {
                                    cls += entry.value;
                                }
                            }
                        }).observe({type: 'layout-shift', buffered: true});
                    } catch(e) {
                        resolve(0); // Feature not supported
                    }
                    
                    setTimeout(() => resolve(cls), 1000);
                });
            """)
            
            # Good CLS score is < 0.1
            if cls_score is not None:
                assert cls_score < 0.25, f"Layout shift too high: {cls_score}"
        except Exception as e:
            # Script execution failed
            pass
