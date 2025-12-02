from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import allure
from utils.logger import logger

class ActionChainsHelper:
    """Helper para ActionChains con evidencias visuales"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)
    
    @allure.step("Click con evidencias visuales en: {element_name}")
    def click_with_evidence(self, locator, element_name):
        """Click con highlight y evidencias"""
        try:
            # Esperar elemento
            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )
            
            # Scroll al elemento
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                element
            )
            time.sleep(0.2)
            
            # Highlight temporal
            original_style = element.get_attribute("style") or ""
            self.driver.execute_script(
                """
                arguments[0].style.border = '3px solid #FF0000';
                arguments[0].style.boxShadow = '0 0 10px #FF0000';
                arguments[0].style.transition = 'all 0.3s';
                """,
                element
            )
            
            # Pausa para evidenciar
            time.sleep(0.3)
            
            # Hover sobre el elemento
            self.actions.move_to_element(element).perform()
            time.sleep(0.2)
            
            # Restaurar estilo
            self.driver.execute_script(
                f"arguments[0].style = '{original_style}';",
                element
            )
            
            # Click con ActionChains
            self.actions.click(element).perform()
            
            logger.info(f"✅ Click realizado en: {element_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en click con evidencias: {e}")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"error_click_{element_name}",
                attachment_type=allure.attachment_type.PNG
            )
            return False
    
    @allure.step("Mover y hacer click en: {element_name}")
    def move_and_click(self, locator, element_name):
        """Mover al elemento y hacer click"""
        try:
            element = self.wait.until(
                EC.presence_of_element_located(locator)
            )
            
            # Mover al elemento
            self.actions.move_to_element(element).perform()
            time.sleep(0.1)
            
            # Click
            element.click()
            
            logger.info(f"✅ Move and click en: {element_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en move_and_click: {e}")
            return False
    
    @allure.step("Ingresar texto en: {element_name}")
    def send_keys_with_evidence(self, locator, text, element_name):
        """Ingresar texto con evidencias"""
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(locator)
            )
            
            # Scroll y highlight
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                element
            )
            
            # Highlight
            original_style = element.get_attribute("style") or ""
            self.driver.execute_script(
                "arguments[0].style.border = '2px solid #00FF00';",
                element
            )
            
            # Limpiar y enviar texto
            element.clear()
            element.send_keys(text)
            
            # Restaurar estilo
            time.sleep(0.2)
            self.driver.execute_script(
                f"arguments[0].style = '{original_style}';",
                element
            )
            
            logger.info(f"✅ Texto ingresado en {element_name}: {text}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando texto: {e}")
            return False
    
    @allure.step("Seleccionar opción: {option_name}")
    def select_dropdown_option(self, dropdown_locator, option_locator, option_name):
        """Seleccionar opción de dropdown con evidencias"""
        try:
            # Abrir dropdown
            self.click_with_evidence(dropdown_locator, "dropdown")
            time.sleep(0.5)
            
            # Seleccionar opción
            success = self.click_with_evidence(option_locator, option_name)
            
            if success:
                logger.info(f"✅ Opción seleccionada: {option_name}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error seleccionando dropdown: {e}")
            return False