"""
Page Object para selección de servicios adicionales
"""
from selenium.webdriver.common.by import By
import allure
import time
import os
from datetime import datetime
from pages.base_page import BasePage
from utils.logger import logger
from utils.config import Config

class ServicesPage(BasePage):
    """Página de servicios adicionales"""
    
    # ==================== LOCATORS ====================
    
    # Lounges
    LOUNGE_CHECKBOX = (By.ID, "lounge-service")
    LOUNGE_OPTION = (By.XPATH, "//label[contains(text(), 'Avianca Lounge')]")
    
    # Equipaje adicional
    EXTRA_BAGGAGE_CHECKBOX = (By.ID, "extra-baggage")
    BAGGAGE_OPTION_20KG = (By.XPATH, "//label[contains(text(), '20 kg')]")
    BAGGAGE_OPTION_30KG = (By.XPATH, "//label[contains(text(), '30 kg')]")
    
    # Asiento preferencial
    PREFERENTIAL_SEAT_CHECKBOX = (By.ID, "preferential-seat")
    
    # Seguro de viaje
    TRAVEL_INSURANCE_CHECKBOX = (By.ID, "travel-insurance")
    
    # Priority boarding
    PRIORITY_BOARDING_CHECKBOX = (By.ID, "priority-boarding")
    
    # Saltar servicios
    SKIP_SERVICES_BUTTON = (By.XPATH, "//button[contains(text(), 'Skip') or contains(text(), 'Saltar')]")
    
    # Continuar (múltiples selectores)
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(@class,'page_button-primary-flow')]")
    CONTINUE_BUTTON_ALT1 = (By.XPATH, "//button[@id='continue-services']")
    CONTINUE_BUTTON_ALT2 = (By.XPATH, "//button[contains(@class, 'btn-action')]")
    CONTINUE_BUTTON_ALT3 = (By.CSS_SELECTOR, "button.page_button-primary-flow")
    CONTINUE_BUTTON_ALT4 = (By.XPATH, "//button-container//button")
    
    # ==================== MÉTODOS ====================
    
    @allure.step("Seleccionar Avianca Lounge")
    def select_avianca_lounge(self):
        """Seleccionar servicio de Avianca Lounge"""
        logger.info("Seleccionando Avianca Lounge")
        
        success = self.click(self.LOUNGE_CHECKBOX, "Checkbox Lounge")
        
        if success:
            time.sleep(0.5)
            success = self.click(self.LOUNGE_OPTION, "Opción Avianca Lounge")
        
        return success
    
    @allure.step("Seleccionar equipaje adicional: {weight} kg")
    def select_extra_baggage(self, weight=20):
        """Seleccionar equipaje adicional"""
        logger.info(f"Seleccionando equipaje adicional: {weight}kg")
        
        success = self.click(self.EXTRA_BAGGAGE_CHECKBOX, "Checkbox equipaje")
        
        if success:
            time.sleep(0.5)
            if weight == 20:
                success = self.click(self.BAGGAGE_OPTION_20KG, "20kg equipaje")
            elif weight == 30:
                success = self.click(self.BAGGAGE_OPTION_30KG, "30kg equipaje")
        
        return success
    
    @allure.step("Seleccionar asiento preferencial")
    def select_preferential_seat(self):
        """Seleccionar asiento preferencial"""
        logger.info("Seleccionando asiento preferencial")
        return self.click(self.PREFERENTIAL_SEAT_CHECKBOX, "Asiento preferencial")
    
    @allure.step("Seleccionar seguro de viaje")
    def select_travel_insurance(self):
        """Seleccionar seguro de viaje"""
        logger.info("Seleccionando seguro de viaje")
        return self.click(self.TRAVEL_INSURANCE_CHECKBOX, "Seguro de viaje")
    
    @allure.step("Seleccionar priority boarding")
    def select_priority_boarding(self):
        """Seleccionar priority boarding"""
        logger.info("Seleccionando priority boarding")
        return self.click(self.PRIORITY_BOARDING_CHECKBOX, "Priority boarding")
    
    @allure.step("Seleccionar cualquier servicio disponible")
    def select_any_service(self):
        """Seleccionar cualquier servicio disponible"""
        logger.info("Seleccionando cualquier servicio")
        
        # Intentar seleccionar lounge
        if self.select_avianca_lounge():
            return True
        
        # Si no hay lounge, intentar con equipaje
        if self.select_extra_baggage():
            return True
        
        # Si no hay equipaje, intentar con seguro
        if self.select_travel_insurance():
            return True
        
        logger.warning("No se encontraron servicios disponibles")
        return False
    
    @allure.step("Saltar todos los servicios")
    def skip_all_services(self):
        """Saltar todos los servicios adicionales"""
        logger.info("Saltando todos los servicios")
        
        # Intentar click en botón skip si existe
        if self.wait_for_element(self.SKIP_SERVICES_BUTTON, "Botón skip", timeout=3):
            return self.click(self.SKIP_SERVICES_BUTTON, "Saltar servicios")
        
        # Si no hay botón skip, simplemente continuar
        logger.info("No hay botón skip, continuando...")
        return True
    
    @allure.step("Continuar a selección de asientos")
    def continue_to_seatmap(self):
        """Continuar a la página de selección de asientos con múltiples selectores"""
        logger.info("Continuando a selección de asientos")
        
        try:
            # Intentar múltiples selectores para el botón continue
            continue_selectors = [
                self.CONTINUE_BUTTON,
                self.CONTINUE_BUTTON_ALT1,
                self.CONTINUE_BUTTON_ALT2,
                self.CONTINUE_BUTTON_ALT3,
                self.CONTINUE_BUTTON_ALT4,
            ]
            
            continue_btn = None
            for selector in continue_selectors:
                try:
                    continue_btn = self.driver.find_element(*selector)
                    if continue_btn:
                        logger.info(f"✓ Botón Continue encontrado con selector: {selector[1]}")
                        break
                except:
                    continue
            
            if not continue_btn:
                logger.error("No se encontró botón Continue en la página de servicios")
                self.take_screenshot("error_continue_button_not_found_services")
                return False
            
            # Scroll al botón
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", continue_btn)
            time.sleep(0.4)

            # Intentar click con ActionChains
            clicked = False
            try:
                from selenium.webdriver.common.action_chains import ActionChains
                actions = ActionChains(self.driver)
                actions.move_to_element(continue_btn).click().perform()
                clicked = True
            except Exception:
                # fallback a JS click
                try:
                    self.driver.execute_script("arguments[0].click();", continue_btn)
                    clicked = True
                except Exception as e:
                    logger.error(f"Error haciendo click (ActionChains y JS) en Continue: {e}")

            if not clicked:
                logger.error("No se pudo hacer click en Continue")
                self.take_screenshot("error_click_continue_to_seatmap")
                return False

            logger.info("✓ Continue button clicked - Navegando a asientos")

            # Esperar a que el mapa de asientos esté disponible (varios selectores posibles)
            seatmap_checks = [
                (By.ID, "seatmap-container"),
                (By.CSS_SELECTOR, "[id*='seatmap']"),
                (By.XPATH, "//*[contains(@class,'seatmap') or contains(@id,'seatmap')]"),
                (By.XPATH, "//div[contains(@class,'seat-economy') or contains(@class,'available') or contains(@class,'seat')]") ,
                (By.TAG_NAME, 'iframe'),
                (By.TAG_NAME, 'canvas')
            ]

            # Aumentar tiempo de espera para la carga dinámica del seatmap
            end = time.time() + 45
            found = False
            while time.time() < end:
                for chk in seatmap_checks:
                    try:
                        el = self.driver.find_element(*chk)
                        if el and el.is_displayed():
                            logger.info(f"✓ Mapa de asientos detectado con selector: {chk}")
                            found = True
                            break
                    except:
                        continue
                if found:
                    break
                time.sleep(0.5)

            if not found:
                logger.error("❌ Timeout esperando elemento: Mapa de asientos")
                # Capturar screenshot y volcado HTML para diagnóstico
                self.take_screenshot("timeout_Mapa de asientos")
                try:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"timeout_services_seatmap_{timestamp}.html"
                    filepath = os.path.join(Config.SCREENSHOT_DIR, filename)
                    os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(self.driver.page_source)
                    logger.info(f"Volcado HTML guardado: {filepath}")
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            allure.attach(f.read(), name="timeout_services_seatmap_html", attachment_type=allure.attachment_type.HTML)
                    except Exception:
                        pass
                except Exception as e:
                    logger.error(f"Error guardando volcado HTML: {e}")
                return False

            return True
            
        except Exception as e:
            logger.error(f"Error en click continuar a asientos: {e}")
            self.take_screenshot("error_click_continue_to_seatmap")
            return False