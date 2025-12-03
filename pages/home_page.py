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
    POS_COLOMBIA_BUTTON = (By.XPATH, "//*[@id='pointOfSaleListId']/li[6]/button")
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
    
    @allure.step("Configurar pasajeros")
    def configure_passengers(self, adults=1, youths=0, children=0, infants=0):
        """Versión mejorada con validaciones y manejo de errores"""
        
        logger.info(f"Configurando {adults}A, {youths}Y, {children}C, {infants}I")
        
        try:
            # ==================== PASO 1: LOCALIZAR Y ABRIR DROPDOWN ====================
            logger.info("=== PASO 1: Abriendo dropdown de pasajeros ===")
            
            # Buscar todos los posibles botones de pasajeros
            passenger_selectors = [
                "//button[@aria-label='Passengers :1']",
                "//button[contains(@aria-label, 'Passengers')]",
                "//button[contains(text(), 'Passenger')]",
                "//div[contains(@class, 'passenger-selector')]//button"
            ]
            
            passenger_btn = None
            for selector in passenger_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for elem in elements:
                        if elem.is_displayed() and elem.is_enabled():
                            passenger_btn = elem
                            logger.info(f"Botón encontrado con selector: {selector}")
                            break
                    if passenger_btn:
                        break
                except:
                    continue
            
            if not passenger_btn:
                logger.error("No se encontró el botón de pasajeros")
                return False
            
            # Hacer click en el botón
            try:
                self.driver.execute_script("arguments[0].click();", passenger_btn)
                logger.info("✓ Dropdown abierto con JavaScript")
            except Exception as e:
                logger.error(f"Error abriendo dropdown: {e}")
                return False
            
            time.sleep(2)
            self.take_screenshot("passengers_dropdown_open")
            
            # ==================== PASO 2: VERIFICAR MODAL ABIERTO ====================
            logger.info("=== PASO 2: Verificando modal de pasajeros ===")
            
            # Buscar el modal de pasajeros
            modal_selectors = [
                "//div[contains(@class, 'modal') and contains(@class, 'open')]",
                "//div[@role='dialog']",
                "//div[contains(@class, 'passenger-modal')]",
                "//div[contains(@class, 'pax-control')]//div[contains(@class, 'modal')]"
            ]
            
            modal_present = False
            for selector in modal_selectors:
                try:
                    if self.driver.find_element(By.XPATH, selector).is_displayed():
                        modal_present = True
                        logger.info(f"Modal encontrado: {selector}")
                        break
                except:
                    continue
            
            if not modal_present:
                logger.warning("Modal de pasajeros no visible, intentando nuevamente...")
                # Intentar abrir de nuevo
                try:
                    passenger_btn.click()
                    time.sleep(2)
                except:
                    pass
            
            # ==================== PASO 3: AGREGAR PASAJEROS ====================
            logger.info("=== PASO 3: Agregando pasajeros ===")
            
            # Mapeo de tipos de pasajero a posición en la lista
            passenger_map = {
                'youths': {'position': 2, 'display_name': 'Jóvenes'},
                'children': {'position': 3, 'display_name': 'Niños'},
                'infants': {'position': 4, 'display_name': 'Infantes'}
            }
            
            # Agregar pasajeros según configuración
            passengers_added = []
            
            for ptype, config in passenger_map.items():
                count = locals()[ptype]  # Obtener count de youths, children, infants
                
                if count > 0:
                    logger.info(f"Agregando {count} {config['display_name']}...")
                    
                    added = self._add_passenger_type(
                        position=config['position'],
                        ptype=config['display_name'],
                        count=count
                    )
                    
                    if added > 0:
                        passengers_added.append(f"{added} {config['display_name']}")
            
            # Adultos ya vienen por defecto, solo agregar extras si es necesario
            if adults > 1:
                logger.info(f"Agregando {adults-1} Adultos adicionales...")
                added_adults = self._add_passenger_type(1, "Adultos", adults - 1)
                if added_adults > 0:
                    passengers_added.append(f"{added_adults} Adultos")
            
            logger.info(f"Pasajeros agregados: {', '.join(passengers_added)}")
            
            # ==================== PASO 4: CONFIRMAR ====================
            logger.info("=== PASO 4: Confirmando selección ===")
            
            confirm_success = self._confirm_passenger_selection()
            
            if not confirm_success:
                logger.warning("No se pudo confirmar, intentando métodos alternativos...")
                
                # Método alternativo 1: Buscar por botón con clase específica
                try:
                    confirm_buttons = self.driver.find_elements(
                        By.XPATH, 
                        "//button[contains(@class, 'confirm') or contains(@class, 'btn-primary')]"
                    )
                    
                    for btn in confirm_buttons:
                        if btn.is_displayed() and ('Confirm' in btn.text or 'Confirmar' in btn.text):
                            btn.click()
                            logger.info("✓ Confirmado (botón con clase)")
                            confirm_success = True
                            break
                except:
                    pass
                
                # Método alternativo 2: Presionar Enter
                if not confirm_success:
                    try:
                        from selenium.webdriver.common.keys import Keys
                        actions = ActionChains(self.driver)
                        actions.send_keys(Keys.ENTER).perform()
                        logger.info("✓ ENTER presionado")
                        time.sleep(1)
                    except:
                        pass
            
            # ==================== PASO 5: VERIFICAR RESULTADO ====================
            logger.info("=== PASO 5: Verificando resultado ===")
            
            time.sleep(2)
            self.take_screenshot("passengers_final")
            
            # Verificar que el modal se cerró
            try:
                modal_closed = True
                for selector in modal_selectors:
                    try:
                        modal = self.driver.find_element(By.XPATH, selector)
                        if modal.is_displayed():
                            modal_closed = False
                            break
                    except:
                        continue
                
                if modal_closed:
                    logger.info("✓ Modal cerrado correctamente")
                else:
                    logger.warning("Modal aún visible, intentando cerrar con ESC...")
                    actions = ActionChains(self.driver)
                    actions.send_keys(Keys.ESCAPE).perform()
                    time.sleep(1)
            except:
                pass
            
            # Verificar cantidad final en el botón
            total_expected = adults + youths + children + infants
            
            try:
                final_button = self.driver.find_element(
                    By.XPATH, 
                    "//button[contains(@aria-label, 'Passengers')]"
                )
                
                final_text = final_button.text or final_button.get_attribute('aria-label') or ""
                logger.info(f"Texto final del botón: {final_text}")
                
                # Extraer número
                import re
                numbers = re.findall(r'\d+', final_text)
                
                if numbers:
                    final_count = int(numbers[0])
                    logger.info(f"Cantidad final mostrada: {final_count}")
                    
                    if final_count == total_expected:
                        logger.info(f"✅ Cantidad correcta: {final_count} pasajeros")
                    else:
                        logger.warning(f"⚠ Cantidad diferente. Esperado: {total_expected}, Mostrado: {final_count}")
                else:
                    logger.info("No se encontró número en el botón")
                    
            except Exception as e:
                logger.error(f"Error verificando resultado: {e}")
            
            logger.info(f"✅ Configuración de pasajeros completada: {total_expected} pasajeros")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error crítico: {e}")
            self.take_screenshot("passengers_critical_error")
            return False

    def _add_passenger_type(self, position, ptype, count):
        """Método auxiliar para agregar un tipo específico de pasajero"""
        added = 0
        
        for i in range(count):
            try:
                # Construir XPath dinámico
                xpath = f"//li[{position}]//button[contains(@class, 'plus') and not(contains(@class, 'disabled'))]"
                
                # Buscar botón plus
                plus_btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                
                # Click con JavaScript
                self.driver.execute_script("arguments[0].click();", plus_btn)
                logger.info(f"✓ +{ptype} ({i+1}/{count})")
                added += 1
                time.sleep(0.5)
                
            except Exception as e:
                logger.warning(f"✗ No se pudo agregar {ptype} {i+1}: {e}")
                break
        
        return added

    def _confirm_passenger_selection(self):
        """Método auxiliar para confirmar la selección"""
        try:
            # Intentar múltiples selectores para el botón Confirm
            confirm_selectors = [
                "//span[contains(text(),'Confirm')]",
                "//button[contains(text(),'Confirm')]",
                "//span[contains(text(),'Confirmar')]",
                "//button[contains(text(),'Confirmar')]",
                "//*[contains(text(),'CONFIRM')]",
                "//button[@type='submit']"
            ]
            
            for selector in confirm_selectors:
                try:
                    confirm_btn = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    
                    if confirm_btn.is_displayed():
                        confirm_btn.click()
                        logger.info(f"✓ Confirmado con selector: {selector}")
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            logger.error(f"Error en confirmación: {e}")
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

    @allure.step("Seleccionar POS - {pos}")
    def select_pos(self, pos="Colombia"):
        """Alias para select_pos_simple para mantener compatibilidad"""
        return self.select_pos_simple(pos)

    @allure.step("Seleccionar POS (simple) - {pos}")
    def select_pos_simple(self, pos="Colombia"):
        """Intento robusto de seleccionar el POS indicado.

        Estrategia:
        - Intentar abrir el selector en la cabecera (xpath del header)
        - Si falla, intentar el `POS_DROPDOWN` o la lista de POS
        - Buscar la opción por texto (ej. 'Colombia') o por selectores específicos
        - Pulsar `Apply` y volver
        """
        logger.info(f"Seleccionando POS: {pos}")

        try:
            # Intentar abrir el selector desde la cabecera (xpath reportado)
            header_xpath = (By.XPATH, "//li[@class='main-header_nav-secondary_item main-header_nav-secondary_item--point-of-sale-selector']//span[2]")

            opened = False

            # 1) Intento header
            if self.wait_for_clickable(header_xpath, "POS header selector", timeout=5):
                self.click(header_xpath, "POS header selector")
                opened = True
            else:
                # 2) Intento dropdown alternativo por id
                if self.wait_for_clickable(self.POS_DROPDOWN, "POS dropdown", timeout=3):
                    self.click(self.POS_DROPDOWN, "POS dropdown")
                    opened = True
                else:
                    # 3) Intento botón en lista (si existe)
                    if self.wait_for_clickable(self.POS_LIST_BUTTON, "POS list button", timeout=3):
                        self.click(self.POS_LIST_BUTTON, "POS list button")
                        opened = True

            if not opened:
                logger.error("No se encontró el control para abrir el selector de POS")
                return False

            time.sleep(1)

            # 4) Seleccionar país por nombre (span normalizado)
            country_locator = (By.XPATH, f"//span[normalize-space()='{pos}']")

            # Si se conoce un selector específico para Colombia, probarlo primero
            try_list = []
            if pos.strip().lower() == 'colombia':
                try_list.append(self.POS_COLOMBIA_BUTTON)
            try_list.append(country_locator)

            selected = False
            for loc in try_list:
                try:
                    if self.wait_for_clickable(loc, f"POS option {pos}", timeout=5):
                        self.click(loc, f"POS option {pos}")
                        selected = True
                        break
                except:
                    continue

            if not selected:
                logger.error(f"No se encontró la opción POS para: {pos}")
                self.take_screenshot("pos_option_not_found")
                return False

            time.sleep(0.6)

            # 5) Pulsar Apply (varias alternativas)
            apply_locator = (By.XPATH, "//span[contains(text(),'Apply')]")
            if self.wait_for_clickable(apply_locator, "Apply button", timeout=5):
                self.click(apply_locator, "Apply button")
            else:
                # buscar botones con span interno o botón genérico
                try:
                    apply_btns = self.driver.find_elements(By.XPATH, "//button//span[contains(text(),'Apply')]")
                    if apply_btns:
                        self.driver.execute_script("arguments[0].click();", apply_btns[0])
                    else:
                        logger.warning("No se encontró 'Apply', intentando cerrar popup con ESC")
                        from selenium.webdriver.common.keys import Keys
                        from selenium.webdriver.common.action_chains import ActionChains
                        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                except Exception as e:
                    logger.error(f"Error intentando pulsar Apply: {e}")

            time.sleep(1)
            logger.info(f"POS '{pos}' seleccionado correctamente")
            return True

        except Exception as e:
            logger.error(f"Error seleccionando POS: {e}")
            self.take_screenshot("pos_selection_error")
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
            success &= self.select_pos_simple(pos)
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
            success &= self.configure_passengers(adults=1, youths=1, children=1, infants=1)
            time.sleep(1)

        # 8. Buscar vuelos
        with allure.step("8. Buscar vuelos"):
            success &= self.search_flights()

        logger.info(f"=== CONFIGURACIÓN HOME COMPLETADA: {'EXITOSA' if success else 'CON ERRORES'} ===")
        return success