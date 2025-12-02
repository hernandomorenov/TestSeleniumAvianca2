import time
from selenium.webdriver.common.by import By
import allure
from pages.base_page import BasePage
from utils.config import Config
from utils.logger import logger

class HomePage(BasePage):
    """Página de inicio de Avianca"""
    
    # ==================== SELECTORES  ====================
    
    # Idioma (CSV paso 2)
    LANGUAGE_DROPDOWN = (By.XPATH, "//span[@class='dropdown_trigger_value']")
    LANGUAGE_ENGLISH_OPTION = (By.XPATH, "//span[contains(text(),'English')]")
    
    # Trip type (CSV paso 4)
    ONE_WAY_RADIO = (By.XPATH, "//input[@id='journeytypeId_1']")
    
    # Destination (CSV pasos 5-7)
    DESTINATION_CONTAINER = (By.XPATH, "//div[@class='station-control station-control--has-filter']")
    DESTINATION_INPUT = (By.XPATH, "//input[@id='arrivalStationInputId']")
    DESTINATION_COLOMBIA_OPTION = (By.XPATH, "//span[contains(text(),'Colombia')]")
    
    # Passengers (CSV pasos 11-17)
    PASSENGER_BUTTON = (By.XPATH, "//button[@aria-label='Passengers :1']")
    PASSENGER_PLUS_BUTTONS = (By.XPATH, "//button[contains(@class, 'ui-num-ud_button plus') and not(contains(@class, 'disabled'))]")
    PASSENGER_CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(), 'Confirm') or contains(@class, 'confirm')]")
    
    # Search (CSV paso 18)
    SEARCH_BUTTON = (By.XPATH, "//button[@id='searchButton']//span[contains(text(), 'Search')]")
    
    # ==================== SELECTORES ORIGINALES ====================
    
    # Idioma original
    LANGUAGE_DROPDOWN_ORIG = (By.ID, "language-selector")
    LANGUAGE_SPANISH = (By.XPATH, "//option[@value='es' or contains(text(), 'Español')]")
    LANGUAGE_ENGLISH = (By.XPATH, "//option[@value='en' or contains(text(), 'English')]")
    LANGUAGE_FRENCH = (By.XPATH, "//option[@value='fr' or contains(text(), 'Français')]")
    LANGUAGE_PORTUGUESE = (By.XPATH, "//option[@value='pt' or contains(text(), 'Português')]")
    
    # POS (País)
    POS_DROPDOWN = (By.ID, "pointOfSaleSelectorId")
    POS_SPAIN = (By.XPATH, "//option[contains(text(), 'Spain') or @value='ES']")
    POS_CHILE = (By.XPATH, "//option[contains(text(), 'Chile') or @value='CL']")
    POS_FRANCE = (By.XPATH, "//option[contains(text(), 'France') or @value='FR']")
    POS_COLOMBIA = (By.XPATH, "//option[contains(text(), 'Colombia') or @value='CO']")
    POS_MEXICO = (By.XPATH, "//option[contains(text(), 'Mexico') or @value='MX']")
    POS_PERU = (By.XPATH, "//option[contains(text(), 'Peru') or @value='PE']")
    
    # Origen y destino originales
    ORIGIN_INPUT = (By.XPATH, "//*[@id='departureStationInputId']")
    ORIGIN_OPTION = (By.XPATH, "//li[contains(text(), 'BOG')]")
    DESTINATION_OPTION = (By.XPATH, "//li[contains(text(), 'MDE')]")
    
    # Pasajeros originales
    PASSENGER_DROPDOWN = (By.ID, "passenger-selector")
    ADULT_PLUS = (By.XPATH, "//button[contains(@class, 'adult-plus')]")
    YOUTH_PLUS = (By.XPATH, "//button[contains(@class, 'youth-plus')]")
    CHILD_PLUS = (By.XPATH, "//button[contains(@class, 'child-plus')]")
    INFANT_PLUS = (By.XPATH, "//button[contains(@class, 'infant-plus')]")
    
    # ==================== MÉTODOS SEGÚN CSV ====================
    
    @allure.step("Select language - English")
    def select_language_english(self):
        """Seleccionar idioma inglés """
        logger.info("Seleccionando idioma English según CSV")
        
        try:
            # Click en dropdown de idioma (Español)
            self.click(self.LANGUAGE_DROPDOWN, "Language dropdown")
            
            # Click en English
            self.click(self.LANGUAGE_ENGLISH_OPTION, "English option")
            
            return True
        except Exception as e:
            logger.error(f"Error seleccionando idioma: {e}")
            return False
    
    @allure.step("Select one way (CSV paso 4)")
    def select_one_way_csv(self):
        """Seleccionar one way específicamente para el CSV"""
        logger.info("Seleccionando One way según CSV paso 4")
        
        try:
            print("=== INTENTANDO SELECCIONAR ONE WAY ===")
            
            # PRIMER INTENTO: Usar el selector del CSV
            print("1. Usando selector del CSV...")
            one_way_css = driver.find_element(By.CSS_SELECTOR, "#journeytypeId_1")
            one_way_css.click()
            time.sleep(1)
            
            if one_way_css.is_selected():
                print("✓ One way seleccionado con selector CSS")
                return True
            
            # SEGUNDO INTENTO: Usar JavaScript
            print("2. Usando JavaScript...")
            self.driver.execute_script("""
                document.querySelector('#journeytypeId_1').checked = true;
                document.querySelector('#journeytypeId_1').dispatchEvent(new Event('change'));
            """)
            time.sleep(1)
            
            if one_way_css.is_selected():
                print("✓ One way seleccionado con JavaScript")
                return True
            
            # TERCER INTENTO: Buscar todas las opciones
            print("3. Buscando todas las opciones...")
            all_radios = self.driver.find_elements(By.XPATH, "//input[contains(@id, 'journeytypeId')]")
            print(f"Encontrados {len(all_radios)} radio buttons")
            
            for radio in all_radios:
                radio_id = radio.get_attribute('id')
                radio_value = radio.get_attribute('value')
                print(f"Radio: id={radio_id}, value={radio_value}")
                
                if '1' in radio_id or (radio_value and 'one' in radio_value.lower()):
                    print(f"Encontrado one way: {radio_id}")
                    radio.click()
                    time.sleep(1)
                    if radio.is_selected():
                        print("✓ One way seleccionado en búsqueda general")
                        return True
            
            # CUARTO INTENTO: Buscar por name
            print("4. Buscando por name...")
            try:
                journey_type_radios = self.driver.find_elements(By.NAME, "journeyType")
                for radio in journey_type_radios:
                    value = radio.get_attribute('value')
                    if value == '1' or (value and 'one' in value.lower()):
                        radio.click()
                        time.sleep(1)
                        if radio.is_selected():
                            print("✓ One way seleccionado por name")
                            return True
            except:
                pass
            
            print("✗ No se pudo seleccionar One way después de todos los intentos")
            # Tomar screenshot para debug
            self.take_screenshot("one_way_failed")
            return False
            
        except Exception as e:
            logger.error(f"Error crítico seleccionando One way: {e}")
            print(f"Error detallado: {e}")
            # Tomar screenshot
            self.take_screenshot("one_way_error")
            return False
    
    @allure.step("Configure destination MDE")
    def configure_destination(self):
        """Configurar destino MDE """
        logger.info("Configurando destino MDE")
        
        try:
            # Click en contenedor de destino
            self.click(self.DESTINATION_CONTAINER, "Destination container")
            
            # Ingresar MDE
            self.enter_text(self.DESTINATION_INPUT, "MDE", "Destination MDE")
            
            # Esperar opciones
            self.wait(2)
            
            # Intentar seleccionar Colombia si aparece
            try:
                self.click(self.DESTINATION_COLOMBIA_OPTION, "Colombia option")
            except:
                logger.info("Opción Colombia no encontrada, continuando...")
            
            return True
        except Exception as e:
            logger.error(f"Error configurando destino: {e}")
            return False
    
    @allure.step("Configure passengers all types")
    def configure_passengers_all_types_csv(self):
        """Configurar pasajeros de todos los tipos """
        logger.info("Configurando pasajeros de todos los tipos")
        
        try:
            # Click en botón de pasajeros (dos veces según CSV)
            self.click(self.PASSENGER_BUTTON, "Passenger button - first click")
            self.wait(0.5)
            self.click(self.PASSENGER_BUTTON, "Passenger button - second click")
            self.wait(1)
            
            # Buscar y hacer click en botones plus para diferentes tipos
            plus_buttons = self.find_elements(self.PASSENGER_PLUS_BUTTONS)
            
            # Añadir pasajeros adicionales (asumiendo orden: adult, youth, child, infant)
            if len(plus_buttons) >= 1:
                plus_buttons[0].click()  # Añadir adulto
                self.wait(0.5)
            
            if len(plus_buttons) >= 2:
                plus_buttons[1].click()  # Añadir joven
                self.wait(0.5)
            
            if len(plus_buttons) >= 3:
                plus_buttons[2].click()  # Añadir niño
                self.wait(0.5)
            
            if len(plus_buttons) >= 4:
                plus_buttons[3].click()  # Añadir infante
                self.wait(0.5)
            
            # Confirmar selección
            try:
                self.click(self.PASSENGER_CONFIRM_BUTTON, "Confirm passengers")
            except:
                # Si no hay botón Confirm, hacer click fuera
                logger.info("Cerrando selector de pasajeros")
                self.click_by_coordinates(10, 10)  # Click en área fuera
            
            return True
        except Exception as e:
            logger.error(f"Error configurando pasajeros: {e}")
            return False
    
    @allure.step("Search flights CSV (CSV paso 18)")
    def search_flights_csv(self):
        """Buscar vuelos según CSV"""
        logger.info("Buscando vuelos según CSV")
        return self.click(self.SEARCH_BUTTON, "Search flights")
    
    @allure.step("Complete home page configuration according to CSV")
    def complete_home_configuration_csv(self):
        """Completar configuración en home page """
        logger.info("Completando configuración home según CSV")
        
        success = True
        
        # Seleccionar idioma English
        success &= self.select_language_english()
        
        # Seleccionar one way
        success &= self.select_one_way()
        
        # Configurar destino
        success &= self.configure_destination_mde_csv()
        
        # Configurar pasajeros
        success &= self.configure_passengers_all_types_csv()
        
        # Buscar vuelos
        success &= self.search_flights_csv()
        
        return success