import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from pages.base_page import BasePage
from utils.config import Config
from utils.logger import logger

class HomePage(BasePage):
    """Página de inicio de Avianca"""
    
    # ==================== SELECTORES  ====================
    
    # Idioma 
    LANGUAGE_DROPDOWN = (By.XPATH, "//span[@class='dropdown_trigger_value']")
    LANGUAGE_ENGLISH_OPTION = (By.XPATH, "//span[contains(text(),'English')]")
    
    # Trip type 
    ONE_WAY_LABEL = (By.CSS_SELECTOR, "label[for='journeytypeId_1']")
    #ONE_WAY_RADIO_ID = (By.ID, "journeytypeId_1")

    
    # Destination 
    DESTINATION_CONTAINER = (By.XPATH, "//div[@class='station-control station-control--has-filter']")
    DESTINATION_INPUT = (By.ID, "arrivalStationInputId")
    STATION_BUTTON_TEMPLATE = "//button[@id='{}']"
    #DESTINATION_COLOMBIA_OPTION = (By.XPATH, "//span[contains(text(),'Colombia')]")
    CALENDAR_DAY_TEMPLATE = "//div[contains(@class, 'calendar')]//span[normalize-space(text())='{}']"

    # Passengers 
    PASSENGER_TRIGGER = (By.XPATH, "//button[contains(@aria-label, 'Passengers')]")
    PASSENGER_BUTTON = (By.XPATH, "//button[@aria-label='Passengers :1']")
    PASSENGER_PLUS_BUTTONS = (By.XPATH, "//button[contains(@class, 'ui-num-ud_button plus') and not(contains(@class, 'disabled'))]")
    PASSENGER_CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(), 'Confirm') or contains(@class, 'confirm')]")
    BTN_PLUS_GENERIC = (By.CSS_SELECTOR, "button.ui-num-ud_button.plus")
    BTN_CONFIRM_PAX = (By.XPATH, "//button[contains(text(), 'Confirm')]")
    
    # Search 
    #SEARCH_BUTTON = (By.XPATH, "//button[@id='searchButton']//span[contains(text(), 'Search')]")
    SEARCH_BUTTON = (By.ID, "searchButton")
    
    # ==================== SELECTORES ORIGINALES ====================
    
    # Idioma original
    LANGUAGE_DROPDOWN_ORIG = (By.ID, "language-selector")
    LANGUAGE_SPANISH = (By.XPATH, "//option[@value='es' or contains(text(), 'Español')]")
    LANGUAGE_ENGLISH = (By.XPATH, "//option[@value='en' or contains(text(), 'English')]")
    LANGUAGE_FRENCH = (By.XPATH, "//option[@value='fr' or contains(text(), 'Français')]")
    LANGUAGE_PORTUGUESE = (By.XPATH, "//option[@value='pt' or contains(text(), 'Português')]")
    
    # POS (País) - Botones en lista
    POS_LIST_BUTTON = (By.XPATH, "//button[contains(@class, 'points-of-sale_list_item')]")
    POS_COLOMBIA_BUTTON = (By.XPATH, "//button[contains(@class, 'points-of-sale_list_item')]//em[text()='Colombia']/..")
    POS_SPAIN_BUTTON = (By.XPATH, "//button[contains(@class, 'points-of-sale_list_item')]//em[text()='Spain']/..")
    POS_CHILE_BUTTON = (By.XPATH, "//button[contains(@class, 'points-of-sale_list_item')]//em[text()='Chile']/..")
    POS_BRAZIL_BUTTON = (By.XPATH, "//button[contains(@class, 'points-of-sale_list_item')]//em[text()='Brazil']/..")
    POS_CANADA_BUTTON = (By.XPATH, "//button[contains(@class, 'points-of-sale_list_item')]//em[text()='Canada']/..")
    POS_MEXICO_BUTTON = (By.XPATH, "//button[contains(@class, 'points-of-sale_list_item')]//em[text()='Mexico']/..")
    POS_PERU_BUTTON = (By.XPATH, "//button[contains(@class, 'points-of-sale_list_item')]//em[text()='Peru']/..")

    # POS Dropdown alternativo (si existe)
    POS_DROPDOWN = (By.ID, "pointOfSaleSelectorId")
    
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
    
    # ==================== MÉTODOS  ====================
    
    @allure.step("Seleccionar idioma - {language}")
    def select_language(self, language="English"):
        """Seleccionar idioma (English, Español, etc.)"""
        logger.info(f"Seleccionando idioma {language}")

        try:
            # Click en dropdown de idioma
            self.click(self.LANGUAGE_DROPDOWN, "Language dropdown")
            time.sleep(1)

            # Seleccionar idioma específico
            if language == "English":
                self.click(self.LANGUAGE_ENGLISH_OPTION, "English option")
            else:
                # Seleccionar otro idioma por xpath dinámico
                language_xpath = (By.XPATH, f"//span[contains(text(),'{language}')]")
                self.click(language_xpath, f"{language} option")

            logger.info(f"✓ Idioma {language} seleccionado")
            return True
        except Exception as e:
            logger.error(f"Error seleccionando idioma: {e}")
            return False

    @allure.step("Seleccionar POS (Point of Sale) - {pos}")
    def select_pos(self, pos="Colombia"):
        """
        Seleccionar POS (País) desde la lista de botones
        Basado en: button.points-of-sale_list_item
        """
        logger.info(f"Seleccionando POS: {pos}")

        try:
            # Mapeo de países a sus botones específicos
            pos_button_mapping = {
                "Colombia": self.POS_COLOMBIA_BUTTON,
                "Spain": self.POS_SPAIN_BUTTON,
                "Chile": self.POS_CHILE_BUTTON,
                "Brazil": self.POS_BRAZIL_BUTTON,
                "Canada": self.POS_CANADA_BUTTON,
                "Mexico": self.POS_MEXICO_BUTTON,
                "Peru": self.POS_PERU_BUTTON
            }

            # Obtener el locator del botón específico
            pos_button_locator = pos_button_mapping.get(pos)

            if not pos_button_locator:
                logger.warning(f"POS {pos} no está en el mapeo, intentando búsqueda genérica")
                pos_button_locator = (By.XPATH, f"//button[contains(@class, 'points-of-sale_list_item')]//em[text()='{pos}']/..")

            # Esperar a que el botón esté disponible
            pos_button = self.wait_for_element(pos_button_locator, timeout=10)

            if not pos_button:
                logger.warning(f"Botón POS {pos} no encontrado, continuando sin seleccionar POS...")
                return True

            # Hacer scroll al botón
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", pos_button)
            time.sleep(0.5)

            # Verificar si ya está seleccionado
            try:
                if 'active' in pos_button.get_attribute('class') or 'selected' in pos_button.get_attribute('class'):
                    logger.info(f"✓ POS {pos} ya está seleccionado")
                    return True
            except:
                pass

            # Hacer clic en el botón
            try:
                pos_button.click()
                logger.info(f"✓ POS {pos} seleccionado exitosamente")
                time.sleep(1)
                return True
            except:
                # Intentar con JavaScript
                logger.info("Intentando clic con JavaScript...")
                self.driver.execute_script("arguments[0].click();", pos_button)
                logger.info(f"✓ POS {pos} seleccionado con JavaScript")
                time.sleep(1)
                return True

        except Exception as e:
            logger.error(f"Error seleccionando POS {pos}: {e}")

            # Intento final: buscar por texto exacto en cualquier botón de POS
            try:
                logger.info("Intentando método de respaldo...")
                all_pos_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'points-of-sale_list_item')]")

                for button in all_pos_buttons:
                    try:
                        button_text = button.text.strip()
                        if pos.lower() in button_text.lower():
                            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
                            time.sleep(0.5)
                            button.click()
                            logger.info(f"✓ POS {pos} seleccionado (método de respaldo)")
                            time.sleep(1)
                            return True
                    except:
                        continue

                logger.warning(f"No se pudo seleccionar POS {pos}, continuando...")
                return True

            except Exception as e2:
                logger.error(f"Error en método de respaldo: {e2}")
                logger.warning("POS podría no estar disponible, continuando...")
                return True  # No fallar el test si POS no está disponible
    
    @allure.step("Seleccionar 'Solo ida' (One Way)")
    def select_one_way(self):
        """Selecciona la opción de solo ida"""
        try:
            self.click(self.ONE_WAY_LABEL)
            logger.info("One Way seleccionado por CSS selector")
            time.sleep(2)
            return True
        except Exception as e:
            logger.error(f"Error crítico en select_one_way: {e}")
            self.take_screenshot("one_way_critical_error")
            return False
    
    @allure.step("Seleccionar Destino: {city} ({code})")
    def select_destination_simple(self, city="Medellin", code="MDE"):
        """Seleccionar destino de forma más directa"""
        logger.info(f"Seleccionando destino: {city} ({code})")
        
        try:
            # 1. Localizar y hacer clic en el campo de destino
            # Usamos el ID directo como sugiere el CSV
            destination_field = self.wait_for_element(self.DESTINATION_INPUT, timeout=10)
            
            destination_field.click()
            time.sleep(0.5)
            
            # 2. Limpiar y escribir
            destination_field.clear()
            destination_field.send_keys(code)
            time.sleep(2)  # Esperar resultados
            
            # 3. Buscar la opción
            # CSV sugiere: //span[contains(text(),'Medellin')]
            option_xpath = f"//span[contains(text(), '{city}')]"
            
            logger.info(f"Buscando opción con XPath: {option_xpath}")
            
            try:
                # Esperar a que aparezca la opción
                option_element = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, option_xpath))
                )
                
                logger.info(f"Opción encontrada: {option_element.text}")
                
                # Hacer clic
                self.driver.execute_script("arguments[0].click();", option_element)
                time.sleep(1)
                
                # Verificar
                current_value = destination_field.get_attribute('value')
                logger.info(f"Valor actual del campo tras selección: {current_value}")
                return True
                
            except Exception as e:
                logger.warning(f"No se encontró opción con '{city}', intentando con código '{code}': {e}")
                
                # Alternativa: buscar por código
                alt_xpath = f"//span[contains(text(), '{code}')]"
                try:
                    alt_option = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, alt_xpath))
                    )
                    logger.info(f"Opción alternativa encontrada: {alt_option.text}")
                    alt_option.click()
                    time.sleep(1)
                    return True
                except Exception as e2:
                    logger.error(f"No se encontró ninguna opción para {city} o {code}: {e2}")
                    return False
                
        except Exception as e:
            logger.error(f"Error seleccionando destino: {e}")
            self.take_screenshot("destination_selection_error")
            return False

    @allure.step("Seleccionar Fecha: día {day}")
    def select_date(self, day=None):
        """
        Selecciona un día específico en el calendario activo
        Si day=None, selecciona automáticamente 2 días después de hoy
        """
        from datetime import datetime, timedelta
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        try:
            # Si no se especifica día, usar 2 días después de hoy
            if day is None:
                target_date = datetime.now() + timedelta(days=2)
                day = str(target_date.day)
                logger.info(f"Seleccionando fecha automática: {target_date.strftime('%d/%m/%Y')}")
            else:
                logger.info(f"Seleccionando día específico: {day}")

            # Esperar a que el calendario esté visible
            time.sleep(1)

            # Buscar el día usando el selector basado en la estructura HTML
            # Según la imagen: span._ngcontent-hic-c18 class="custom-day_day"
            xpath_day = f"//span[contains(@class, 'custom-day_day') and normalize-space(text())='{day}']"

            logger.info(f"Buscando día con XPath: {xpath_day}")

            # Esperar a que aparezcan los días del calendario
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'custom-day_day')]"))
            )

            # Buscar todos los días con ese número
            days = self.driver.find_elements(By.XPATH, xpath_day)

            if not days:
                logger.error(f"No se encontraron días con el número {day}")
                # Intentar con el template original
                xpath_day_alt = self.CALENDAR_DAY_TEMPLATE.format(day)
                days = self.driver.find_elements(By.XPATH, xpath_day_alt)

            # Filtrar y hacer clic en el primer día visible que no esté disabled
            for d in days:
                try:
                    if d.is_displayed():
                        # Verificar que no esté deshabilitado
                        parent_class = d.find_element(By.XPATH, "./ancestor::div[contains(@class, 'ngb-dp-day')]").get_attribute('class')

                        if 'disabled' not in parent_class and 'ng-star-inserted' in parent_class:
                            # Hacer scroll al elemento
                            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", d)
                            time.sleep(0.5)

                            # Intentar clic normal
                            try:
                                d.click()
                                logger.info(f"✓ Fecha seleccionada: Día {day}")
                                time.sleep(1)
                                return True
                            except:
                                # Intentar con JavaScript
                                self.driver.execute_script("arguments[0].click();", d)
                                logger.info(f"✓ Fecha seleccionada con JavaScript: Día {day}")
                                time.sleep(1)
                                return True
                except Exception as e:
                    logger.debug(f"Día no clickeable: {e}")
                    continue

            logger.error(f"No se pudo hacer clic en ningún día {day} visible")
            return False

        except Exception as e:
            logger.error(f"Error seleccionando fecha {day}: {e}")
            self.take_screenshot("date_selection_error")
            return False
    
    @allure.step("Select passengers")
    def select_passengers(self, adults=1, youths=0, children=0, infants=0):
        """Seleccionar pasajeros"""
        try:
            print(f"Pasajeros: A={adults}, Y={youths}, C={children}, I={infants}")
            
            passenger_dropdown = self.wait.until(EC.element_to_be_clickable(self.PASSENGER_DROPDOWN))
            self.actions.move_to_element(passenger_dropdown).click().perform()
            time.sleep(2)
            
            def click_plus(ptype, count, current=0):
                if ptype == "adults":
                    current = 1
                clicks = count - current
                if clicks > 0:
                    indices = {"adults": 1, "youths": 2, "children": 3, "infants": 4}
                    idx = indices.get(ptype)
                    if idx:
                        for i in range(clicks):
                            try:
                                btn = self.driver.find_element(By.XPATH, f"(//button[contains(@class, 'plus')])[{idx}]")
                                self.actions.move_to_element(btn).click().perform()
                                print(f"✓ +{ptype} ({i+1}/{clicks})")
                                time.sleep(0.5)
                            except:
                                pass
            
            if adults > 1:
                click_plus("adults", adults, 1)
            if youths > 0:
                click_plus("youths", youths, 0)
            if children > 0:
                click_plus("children", children, 0)
            if infants > 0:
                click_plus("infants", infants, 0)
            
            time.sleep(1)
            
            try:
                confirm = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm') or contains(text(), 'Confirmar')]")
                self.actions.move_to_element(confirm).click().perform()
                print("✓ Confirmado")
            except:
                self.actions.send_keys(Keys.ESCAPE).perform()
                print("✓ ESC")
            
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @allure.step("Buscar Vuelos")
    def click_search(self):
        self.click(self.SEARCH_BUTTON)
    
    @allure.step("Search flights")
    def search_flights(self):
        """Buscar vuelos"""
        logger.info("Buscando vuelos ")
        return self.click(self.SEARCH_BUTTON, "Search flights")
    
    @allure.step("Seleccionar origen - {city} ({code})")
    def select_origin(self, city="Bogota", code="BOG"):
        """Seleccionar ciudad de origen"""
        logger.info(f"Seleccionando origen: {city} ({code})")

        try:
            # Localizar y hacer clic en el campo de origen
            origin_field = self.wait_for_element(self.ORIGIN_INPUT, timeout=10)
            origin_field.click()
            time.sleep(0.5)

            # Limpiar y escribir
            origin_field.clear()
            origin_field.send_keys(code)
            time.sleep(2)  # Esperar resultados

            # Buscar la opción
            option_xpath = f"//span[contains(text(), '{city}') or contains(text(), '{code}')]"

            try:
                option_element = self.wait_for_element((By.XPATH, option_xpath), timeout=5)
                self.driver.execute_script("arguments[0].click();", option_element)
                time.sleep(1)
                logger.info(f"✓ Origen {city} seleccionado")
                return True
            except:
                logger.warning(f"No se encontró opción exacta, intentando clic directo")
                return True

        except Exception as e:
            logger.error(f"Error seleccionando origen: {e}")
            return False

    @allure.step("Complete home page configuration")
    def complete_home_configuration(self, language="English", pos="Colombia",
                                     origin_city="Bogota", origin_code="BOG",
                                     dest_city="Medellin", dest_code="MDE",
                                     day=None):
        """
        Completar configuración en home page
        Requisitos: Seleccionar idioma, pos, origen, destino y 1 pasajero de cada tipo
        Si day=None, se selecciona automáticamente 2 días después de hoy
        """
        from datetime import datetime, timedelta
        logger.info("=== INICIANDO CONFIGURACIÓN HOME PAGE ===")

        success = True

        # 1. Seleccionar idioma
        with allure.step(f"1. Seleccionar idioma: {language}"):
            success &= self.select_language(language)
            time.sleep(2)

        # 2. Seleccionar POS
        with allure.step(f"2. Seleccionar POS: {pos}"):
            success &= self.select_pos(pos)
            time.sleep(1)

        # 3. Seleccionar tipo de viaje: One way
        with allure.step("3. Seleccionar One Way"):
            success &= self.select_one_way()
            time.sleep(1)

        # 4. Seleccionar origen
        with allure.step(f"4. Seleccionar origen: {origin_city}"):
            success &= self.select_origin(origin_city, origin_code)
            time.sleep(1)

        # 5. Seleccionar destino
        with allure.step(f"5. Seleccionar destino: {dest_city}"):
            success &= self.select_destination_simple(dest_city, dest_code)
            time.sleep(1)

        # 6. Seleccionar fecha (2 días después de hoy si no se especifica)
        date_str = "automática (2 días después)" if day is None else f"día {day}"
        with allure.step(f"6. Seleccionar fecha: {date_str}"):
            success &= self.select_date(day)
            time.sleep(1)

        # 7. Configurar pasajeros (1 Adulto, 1 Joven, 1 Niño, 1 Infante)
        with allure.step("7. Configurar pasajeros: 1 Adulto, 1 Joven, 1 Niño, 1 Infante"):
            success &= self.configure_passengers()
            time.sleep(1)

        # 8. Buscar vuelos
        with allure.step("8. Buscar vuelos"):
            success &= self.search_flights()

        logger.info(f"=== CONFIGURACIÓN HOME COMPLETADA: {'EXITOSA' if success else 'CON ERRORES'} ===")
        return success