# pages/flight_selection_page.py
import time
from selenium.webdriver.common.by import By
import allure
from pages.base_page import BasePage
from utils.logger import logger

class FlightSelectionPage(BasePage):
    """Página de selección de vuelos"""
    
    # SELECTORES
    FARE_OPTION = (By.XPATH, "//div[contains(@class, 'fare-card')][1]")
    FARE_PRICE = (By.XPATH, "//div[contains(@class, 'fare-price')]")
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(text(), 'Continue') or contains(text(), 'Continuar')]")
    
    @allure.step("Esperar a que cargue la página de selección de vuelos")
    def wait_for_page_load(self):
        """Esperar a que cargue la página de selección de vuelos"""
        logger.info("Esperando a que cargue la página de selección de vuelos...")
        try:
            # Esperar a que aparezcan las opciones de tarifa
            self.wait_for_element(self.FARE_OPTION, timeout=20)
            logger.info("✓ Página de selección de vuelos cargada")
            return True
        except Exception as e:
            logger.error(f"Error cargando página de selección de vuelos: {e}")
            return False
    
    @allure.step("Seleccionar tarifa Basic")
    def select_fare(self, fare_type="Basic"):
        """
        Seleccionar tarifa específica (por defecto Basic)
        Requisito: Seleccionar tarifa Basic
        """
        logger.info(f"Seleccionando tarifa {fare_type}...")
        try:
            # Primero intentar buscar tarifa por nombre
            fare_xpath = f"//div[contains(@class, 'fare') and contains(., '{fare_type}')]//button"

            try:
                # Intentar encontrar botón de tarifa específica
                fare_button = self.wait_for_element((By.XPATH, fare_xpath), timeout=10)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", fare_button)
                time.sleep(1)
                fare_button.click()
                logger.info(f"✓ Tarifa {fare_type} seleccionada por nombre")
                time.sleep(2)
                return True
            except:
                # Si no se encuentra por nombre, buscar la primera tarifa disponible
                logger.warning(f"No se encontró tarifa {fare_type} por nombre, seleccionando primera disponible")
                fare_options = self.driver.find_elements(*self.FARE_OPTION)

                if not fare_options:
                    logger.error("No se encontraron tarifas disponibles")
                    return False

                # Seleccionar la primera tarifa (generalmente es Basic)
                fare_options[0].click()
                logger.info("✓ Primera tarifa seleccionada (posiblemente Basic)")
                time.sleep(2)
                return True

        except Exception as e:
            logger.error(f"Error seleccionando tarifa: {e}")
            return False
    
    @allure.step("Verificar precio del vuelo")
    def verify_flight_price(self):
        """Verificar y obtener el precio del vuelo"""
        logger.info("Verificando precio del vuelo...")
        try:
            price_element = self.wait_for_element(self.FARE_PRICE, timeout=10)
            price_text = price_element.text.strip()
            
            if price_text:
                logger.info(f"Precio encontrado: {price_text}")
                return price_text
            
            logger.warning("No se encontró texto de precio")
            return None
            
        except Exception as e:
            logger.error(f"Error verificando precio: {e}")
            return None
    
    @allure.step("Continuar a página de pasajeros")  # ✅ NOMBRE CORREGIDO
    def continue_to_passengers(self):
        """Hacer clic en el botón Continuar para ir a pasajeros"""
        logger.info("Continuando a página de pasajeros...")
        try:
            # Buscar botón Continuar
            continue_button = self.wait_for_element(self.CONTINUE_BUTTON, timeout=10)
            
            # Hacer scroll al botón
            self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
            time.sleep(1)
            
            # Hacer clic
            continue_button.click()
            logger.info("✓ Continuando a pasajeros")
            
            # Esperar a que se procese
            time.sleep(3)
            return True
            
        except Exception as e:
            logger.error(f"Error continuando a pasajeros: {e}")
            return False
    
    @allure.step("Seleccionar tarifa específica por nombre")
    def select_specific_fare(self, fare_name="Basic"):
        """Seleccionar una tarifa específica por nombre"""
        logger.info(f"Seleccionando tarifa: {fare_name}")
        try:
            # Buscar tarifa por nombre
            fare_xpath = f"//div[contains(@class, 'fare-card') and contains(., '{fare_name}')]"
            fare_element = self.wait_for_element((By.XPATH, fare_xpath), timeout=10)
            
            fare_element.click()
            logger.info(f"✓ Tarifa {fare_name} seleccionada")
            time.sleep(2)
            return True
            
        except Exception as e:
            logger.error(f"Error seleccionando tarifa {fare_name}: {e}")
            return False