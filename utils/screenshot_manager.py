import os
import allure
from datetime import datetime
from utils.config import Config
from utils.logger import logger

class ScreenshotManager:
    """Gestor de screenshots automáticos"""
    
    def __init__(self, driver):
        self.driver = driver
        os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
    
    @allure.step("Tomar screenshot: {screenshot_name}")
    def take_screenshot(self, screenshot_name):
        """Tomar screenshot y adjuntar a Allure"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{screenshot_name}_{timestamp}.png"
            filepath = os.path.join(Config.SCREENSHOT_DIR, filename)
            
            # Tomar screenshot
            self.driver.save_screenshot(filepath)
            
            # Adjuntar a Allure
            with open(filepath, 'rb') as f:
                allure.attach(
                    f.read(),
                    name=screenshot_name,
                    attachment_type=allure.attachment_type.PNG
                )
            
            logger.info(f"📸 Screenshot tomado: {filename}")
            return filepath
            
        except Exception as e:
            logger.error(f"❌ Error tomando screenshot: {e}")
            return None
    
    def take_screenshot_on_failure(self, test_name):
        """Tomar screenshot cuando un test falla"""
        screenshot_name = f"FAILURE_{test_name}"
        return self.take_screenshot(screenshot_name)
    
    def take_screenshot_on_success(self, test_name):
        """Tomar screenshot cuando un test pasa"""
        screenshot_name = f"SUCCESS_{test_name}"
        return self.take_screenshot(screenshot_name)