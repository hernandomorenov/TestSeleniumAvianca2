from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
import time
from utils.action_chains_helper import ActionChainsHelper
from utils.screenshot_manager import ScreenshotManager
from utils.logger import logger

class BasePage:
    """Clase base con métodos comunes para todas las páginas"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChainsHelper(driver)
        self.screenshots = ScreenshotManager(driver)
    
    # ==================== MÉTODOS COMUNES ====================
    
    @allure.step("Esperar elemento: {element_name}")
    def wait_for_element(self, locator, element_name="elemento", timeout=10):
        """Esperar a que un elemento esté presente"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            logger.info(f"✅ Elemento encontrado: {element_name}")
            return element
        except TimeoutException:
            logger.error(f"❌ Timeout esperando elemento: {element_name}")
            self.screenshots.take_screenshot(f"timeout_{element_name}")
            return None
    
    @allure.step("Esperar elemento clickeable: {element_name}")
    def wait_for_clickable(self, locator, element_name="elemento", timeout=10):
        """Esperar a que un elemento sea clickeable"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            logger.info(f"✅ Elemento clickeable: {element_name}")
            return element
        except TimeoutException:
            logger.error(f"❌ Timeout esperando clickeable: {element_name}")
            return None
    
    @allure.step("Click en: {element_name}")
    def click(self, locator, element_name="elemento"):
        """Click con evidencias"""
        self.screenshots.take_screenshot(f"before_click_{element_name}")
        success = self.actions.click_with_evidence(locator, element_name)
        self.screenshots.take_screenshot(f"after_click_{element_name}")
        return success
    
    @allure.step("Ingresar texto en: {element_name}")
    def enter_text(self, locator, text, element_name="campo"):
        """Ingresar texto con evidencias"""
        self.screenshots.take_screenshot(f"before_text_{element_name}")
        success = self.actions.send_keys_with_evidence(locator, text, element_name)
        self.screenshots.take_screenshot(f"after_text_{element_name}")
        return success
    
    @allure.step("Seleccionar dropdown: {element_name}")
    def select_dropdown(self, dropdown_locator, option_locator, option_name):
        """Seleccionar opción de dropdown"""
        return self.actions.select_dropdown_option(
            dropdown_locator, option_locator, option_name
        )
    
    @allure.step("Esperar página cargada")
    def wait_for_page_load(self, timeout=20):
        """Esperar a que la página cargue completamente"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            logger.info("✅ Página cargada completamente")
            time.sleep(1)  # Pequeña pausa adicional
            return True
        except TimeoutException:
            logger.warning("⚠️  Timeout en carga de página")
            return False
    
    @allure.step("Navegar a URL")
    def navigate_to(self, url):
        """Navegar a una URL"""
        logger.info(f"🌐 Navegando a: {url}")
        self.driver.get(url)
        return self.wait_for_page_load()
    
    @allure.step("Tomar screenshot")
    def take_screenshot(self, name):
        """Tomar screenshot"""
        return self.screenshots.take_screenshot(name)
    
    @allure.step("Obtener título de página")
    def get_page_title(self):
        """Obtener título de la página"""
        return self.driver.title
    
    @allure.step("Obtener URL actual")
    def get_current_url(self):
        """Obtener URL actual"""
        return self.driver.current_url
    
    @allure.step("Verificar texto en página")
    def verify_text_on_page(self, text):
        """Verificar si un texto está en la página"""
        page_source = self.driver.page_source
        return text.lower() in page_source.lower()