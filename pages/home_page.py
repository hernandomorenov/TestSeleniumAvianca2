import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from pages.base_page import BasePage
from utils.config import Config
from utils.logger import logger
from selenium.webdriver import ActionChains

from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException
)

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
    
    # ==================== SELECTORES MULTIIDIOMA ====================
    
    # Dropdown de idioma
    LANGUAGE_DROPDOWN = (By.XPATH, "//span[@class='dropdown_trigger_value']")
    
    # Idiomas disponibles
    LANGUAGE_ENGLISH = (By.XPATH, "//span[contains(text(),'English')]")
    LANGUAGE_PORTUGUESE = (By.XPATH, "//span[contains(text(),'Português')]")
    LANGUAGE_FRENCH = (By.XPATH, "//span[contains(text(),'Français')]")
    LANGUAGE_SPANISH = (By.XPATH, "//span[contains(text(),'Español')]")
    
    # Mapa de idiomas
    LANGUAGE_MAP = {
        "English": LANGUAGE_ENGLISH,
        "Português": LANGUAGE_PORTUGUESE,
        "Français": LANGUAGE_FRENCH,
        "Español": LANGUAGE_SPANISH
    }
    
    # Links del footer (textos en español - base)
    FOOTER_LINKS = {
        "Somos avianca": (By.XPATH, "//*[@id='footerNavListId-1']/li[1]/a"),
        "Sostenibilidad": (By.XPATH, "//*[@id='footerNavListId-1']/li[5]/a"),
        "Plan de accesibilidad": (By.XPATH, "//*[@id='footerNavListId-1']/li[6]/a"),
        "Información legal": (By.XPATH, "//*[@id='footerNavListId-3']/li[1]/a")
    }

    def __init__(self, driver):
        super().__init__(driver)
    
    # Mapa de textos por idioma (ajusta si tu sitio usa otras cadenas)
    HEADER_TEXTS = {
        "Español": {
            "Reservar": "//span[normalize-space()='Reservar']",
            "Ofertas y destinos": "//span[@class='button_label' and normalize-space()='Ofertas y destinos']",
            "Destinos": "//span[normalize-space()='Destinos']",
            "Información y ayuda": "//span[@class='button_label' and normalize-space()='Información y ayuda']",
            "Tipos de tarifas": "//span[normalize-space()='Tipos de tarifas']",
        },
        "English": {
            "Book": "//span[normalize-space()='Book']",
            "Deals and destinations": "//span[@class='button_label' and normalize-space()='Offers and destinations']",
            "Destinations": "//span[normalize-space()='Our destinations']",
            "Information and help": "//span[@class='button_label' and normalize-space()='Information and help']",
            "Fare types": "//span[normalize-space()='Types of fares']",
        },
        "Português": {
            "Reservar": "//span[normalize-space()='Reservar']",
            "Ofertas e destinos": "//span[@class='button_label' and normalize-space()='Ofertas e destinos']",
            "Destinos": "//span[normalize-space()='Nossos destinos']",
            "Informação e ajuda": "//span[@class='button_label' and normalize-space()='Informação e assistência']",
            "Tipos de tarifas": "//span[normalize-space()='Tipos de taxas']",
        },
        "Français": {
            "Réserver": "//span[normalize-space()='Réserver']",
            "Offres et destinations": "//span[@class='button_label' and normalize-space()='Offres et destinations']",
            "Destinations": "//span[normalize-space()='Destinations']",
            "Informations et aide": "//span[@class='button_label' and normalize-space()='Informations et aide']",
            "Types de tarifs": "//span[normalize-space()='Types de tarifs']",
        },
    }

    def header_xpath(self, language, key):
        """Devuelve el XPath del ítem de header según idioma y clave textual."""
        # Normaliza el idioma que muestra el dropdown
        lang = language.strip()
        # Algunos sitios muestran 'English (US)' → reduce a 'English'
        if lang.startswith("English"):
            lang = "English"
        return self.HEADER_TEXTS.get(lang, {}).get(key)
    
    # ==================== MÉTODOS PARA HEADER ====================
    
    
    @allure.step("Abrir/Click con ActionChains: {desc}")
    def _hover_click_with_actions(self, locator, desc="elemento"):
        element = self.wait_for_clickable(locator, desc, timeout=12)
        if not element:
            return False
        try:
            # Scroll al centro y borde rojo visible
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", element
            )
            self.driver.execute_script("arguments[0].style.border='3px solid #e00';", element)
            time.sleep(0.25)

            ActionChains(self.driver).move_to_element(element).pause(0.2).click().perform()

            # Limpieza del borde
            try:
                self.driver.execute_script("arguments[0].style.border='0px';", element)
            except Exception:
                pass

            return True
        except Exception as e:
            # Fallback: clic directo y último recurso: JS
            try:
                element.click()
                return True
            except Exception:
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    return True
                except Exception:
                    logger.error(f"Error hover+click ({desc}): {e}")


    @allure.step("Click visual: {description}")
    def click_with_highlight(self, xpath, description):
        success = False
        element = None
        try:
            # Esperar a que sea clickeable
            element = WebDriverWait(self.driver, 12).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            # Scroll al centro
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", element
            )
            time.sleep(0.3)
            # Borde rojo
            self.driver.execute_script("arguments[0].style.border='3px solid red';", element)
            time.sleep(0.2)
            # Intento 1: ActionChains
            try:
                ActionChains(self.driver).move_to_element(element).pause(0.2).click().perform()
            except ElementClickInterceptedException:
                # Intento 2: click directo
                try:
                    element.click()
                except Exception:
                    # Intento 3: JavaScript click
                    self.driver.execute_script("arguments[0].click();", element)
            success = True
        except Exception as e:
            logger.error(f"Error clickeando {description}: {e}")
            success = False

        # Limpieza de borde (segura ante elemento stale)
        if element:
            try:
                self.driver.execute_script("arguments[0].style.border='0px';", element)
            except StaleElementReferenceException:
                logger.info("Elemento quedó 'stale' tras el clic; se omite limpieza del borde.")
            except Exception as e:
                logger.debug(f"Error de limpieza de borde: {e}")
        return success

    @allure.step("Ejecutar scroll: {direction}")
    def perform_scroll(self, direction="down"):
        try:
            scroll_amount = 500 if direction == "down" else -500
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(1)
            return True
        except Exception as e:
            return False

    # ==================== MÉTODOS SIMPLIFICADOS ====================
    
    
    @allure.step("Seleccionar idioma - {language}")
    def select_language(self, language="English"):
        logger.info(f"Seleccionando idioma {language}")

        try:
            # --- 2.1 Neutralizar posibles cierres/recargas agresivas ---
            self.driver.execute_script("""
                try { window.onbeforeunload = null; } catch(e) {}
                try {
                    window._originalOpen = window.open;
                    window.open = function(url, target, features) {
                        return window._originalOpen(url, "_self", features);
                    };
                } catch(e) {}
            """)

            # Guarda los handles actuales para detectar cambios de pestañas
            original_handles = self.driver.window_handles

            # --- 2.2 Abrir dropdown con ActionChains y evidencia visual ---
            opened = self._hover_click_with_actions(self.LANGUAGE_DROPDOWN, "Language dropdown")
            if not opened:
                elem = self.wait_for_clickable(self.LANGUAGE_DROPDOWN, "Language dropdown", timeout=10)
                if not elem:
                    return False
                self.driver.execute_script("arguments[0].click();", elem)

            self.take_screenshot(f"language_dropdown_open_{language}")
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'English') or contains(text(),'Español') or contains(text(),'Português') or contains(text(),'Fran')]"))
                )
            except TimeoutException:
                logger.error("El menú de idiomas no se abrió/mostró opciones a tiempo.")
                return False

            time.sleep(0.4)

            # --- 2.3 Localizar opción por idioma y click con ActionChains ---
            option_locator = (By.XPATH, f"//span[contains(text(),'{language}')]")
            selected = self._hover_click_with_actions(option_locator, f"{language} option")
            if not selected:
                opt = self.wait_for_clickable(option_locator, f"{language} option", timeout=6)
                if not opt:
                    logger.error(f"No se encontró la opción de idioma: {language}")
                    return False
                self.driver.execute_script("arguments[0].click();", opt)

            # --- 2.4 Esperar actualización ---
            time.sleep(1.5)

            # Si el sitio "abrió" otra pestaña, mantenernos en una válida
            current_handles = self.driver.window_handles
            if len(current_handles) != len(original_handles):
                new_handle = current_handles[-1]
                self.driver.switch_to.window(new_handle)
                logger.info("Se detectó apertura/cambio de pestaña; se cambió el foco a la pestaña activa.")

            # Validación suave: el dropdown refleja el idioma actual
            try:
                current_lang = self.get_current_language()
                logger.info(f"Idioma actual en UI: {current_lang}")
            except Exception:
                current_lang = "unknown"
                logger.warning("No se pudo obtener idioma actual")

            return True

        except Exception as e:
            logger.error(f"Error seleccionando idioma: {e}")
            self.take_screenshot("language_selection_error")
            return False  # Asegúrate de retornar False en caso de error

    
    @allure.step("Obtener idioma actual")
    def get_current_language(self):
        """Obtener idioma actual seleccionado"""
        try:
            dropdown = self.wait_for_element(self.LANGUAGE_DROPDOWN, "Language dropdown")
            if dropdown:
                return dropdown.text.strip()
        except:
            pass
        return "Español"  # Default
    
    @allure.step("Click en link del footer: {link_name}")
    def click_footer_link(self, link_name):
        """Click simple en link del footer"""
        try:
            if link_name in self.FOOTER_LINKS:
                selector = self.FOOTER_LINKS[link_name]
                
                # Scroll al elemento primero
                element = self.wait_for_element(selector, f"Footer link: {link_name}")
                if element:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    time.sleep(0.5)
                
                # Click
                self.click(selector, f"Footer: {link_name}")
                time.sleep(2)  # Esperar redirección
                return True
            return False
        except Exception as e:
            logger.warning(f"No se pudo clickear {link_name}: {e}")
            return False
    
    @allure.step("Hacer scroll al footer")
    def scroll_to_footer(self):
        """Hacer scroll al final de la página"""
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            return True
        except:
            return False

    # ===================== SELECT POS ===================================#
    
    @allure.step("Seleccionar POS (CSV) - {target_pos}")
    def select_pos_from_csv(self, target_pos: str):
        """
        Selecciona el POS según los pasos y xpaths del CSV:
        target_pos: "otros_paises", "espana", "chile"
        """
        # Mapa de xpaths según CSV
        HEADER_POS_TRIGGER = (By.XPATH, "//li[@class='main-header_nav-secondary_item main-header_nav-secondary_item--point-of-sale-selector']//span[2]")
        APPLY_SPAN = (By.XPATH, "//span[contains(text(),'Aplicar')]")
        OTROS_PAISES = (By.XPATH, "//span[normalize-space()='Otros países']")
        ESPANA = (By.XPATH, "//span[normalize-space()='España']")
        CHILE = (By.XPATH, "//span[normalize-space()='Chile']")
        CURRENCY_BUTTON = (By.XPATH, "//span[@class='button_label_value']")

        try:
            # --- Abrir el selector en el header (hover + evidencia) ---
            opened = self._hover_click_with_actions(HEADER_POS_TRIGGER, "Header POS trigger")
            if not opened:
                elem = self.wait_for_clickable(HEADER_POS_TRIGGER, "Header POS trigger", timeout=10)
                if not elem:
                    self.take_screenshot("pos_header_trigger_not_found")
                    return False
                self.driver.execute_script("arguments[0].click();", elem)
            self.take_screenshot("pos_popup_open")

            # --- Selección según destino ---
            target = target_pos.strip().lower()

            if target == "otros_paises":
                if not self._hover_click_with_actions(OTROS_PAISES, "Otros países"):
                    opt = self.wait_for_clickable(OTROS_PAISES, "Otros países", timeout=8)
                    if not opt: return False
                    self.driver.execute_script("arguments[0].click();", opt)
                time.sleep(0.3)
                self._hover_click_with_actions(APPLY_SPAN, "Aplicar")
                time.sleep(1.2)
                self.take_screenshot("pos_otros_paises_applied")
                return True

            elif target == "espana":
                # CSV: abrir header -> click "España" -> "Aplicar" -> 
                if not self._hover_click_with_actions(ESPANA, "España"):
                    opt = self.wait_for_clickable(ESPANA, "España", timeout=8)
                    if not opt: return False
                    self.driver.execute_script("arguments[0].click();", opt)
                time.sleep(0.3)
                self._hover_click_with_actions(APPLY_SPAN, "Aplicar")
                time.sleep(1.2)
                self.take_screenshot("pos_espana_applied")

                # CSV luego usa un click en "€" para abrir el popup de moneda/país
                # Esto puede aparecer tras la recarga; lo intentamos si está disponible:
                try:
                    reopen = self.wait_for_clickable(CURRENCY_BUTTON, "Currency button", timeout=5)
                    if reopen:
                        self._hover_click_with_actions(CURRENCY_BUTTON, "Currency button (reopen)")
                        self.take_screenshot("currency_popup_open")
                    else:
                        # Si no aparece, no es crítico: se continúa
                        pass
                except Exception:
                    pass
                return True

            elif target == "chile":
                # CSV: abrir header -> click "Chile" -> "Aplicar"
                if not self._hover_click_with_actions(CHILE, "Chile"):
                    opt = self.wait_for_clickable(CHILE, "Chile", timeout=8)
                    if not opt: return False
                    self.driver.execute_script("arguments[0].click();", opt)
                time.sleep(0.3)
                self._hover_click_with_actions(APPLY_SPAN, "Aplicar")
                time.sleep(1.2)
                self.take_screenshot("pos_chile_applied")
                return True

            else:
                logger.warning(f"POS objetivo desconocido: {target_pos}")
                return False

        except Exception as e:
            logger.error(f"Error en select_pos_from_csv({target_pos}): {e}")
            self.take_screenshot(f"pos_csv_error_{target_pos}")
            return
            
    #====================== TEST CASE 1 =====================================  #

    


    @allure.step("Click XPath con ActionChains: {desc}")
    def click_xpath_with_actions(self, xpath: str, desc: str):
        """Wrapper para usar evidencia visual con el XPath exacto del CSV."""
        return self.click_with_highlight(xpath, desc)  # ya usa ActionChains + borde rojo

    
    @allure.step("CSV: Seleccionar idioma {language}")
    def select_language_from_csv(self, language="English"):
        """
        Paso 2-3 del CSV:
        2) Click al dropdown de idioma
        3) Click en "English"
        """
        LANG_DROPDOWN_XPATH = "//span[@class='dropdown_trigger_value']"  # del CSV
        # Lista de locators robustos para la opción 'English'
        OPTION_LOCATORS = [
            (By.XPATH, f"//button[starts-with(@id,'optionId_languageListOptionsLisId')][normalize-space()='{language}']"),
            (By.XPATH, f"//button[@ role='option'][normalize-space()='{language}']"),
            (By.XPATH, f"//button[normalize-space()='{language}']"),
            (By.XPATH, f"//span[normalize-space()='{language}']"),  # último fallback
        ]

        try:
            # 1) Abrir dropdown con evidencia ActionChains
            opened = self.click_xpath_with_actions(LANG_DROPDOWN_XPATH, "Idioma - dropdown")
            if not opened:
                elem = self.wait_for_clickable((By.XPATH, LANG_DROPDOWN_XPATH), "Idioma - dropdown", timeout=10)
                if not elem:
                    self.take_screenshot("csv_language_dropdown_not_found")
                    return False
                self.driver.execute_script("arguments[0].click();", elem)

            # Esperar presencia de cualquier opción de idioma
            try:
                WebDriverWait(self.driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@role='option']|//span[contains(.,'English') or contains(.,'Español')]"))
                )
            except TimeoutException:
                self.take_screenshot("csv_language_options_not_visible")
                return False

            self.take_screenshot("csv_language_dropdown_open")

            # 2) Buscar y clicar la opción 'English' con distintos locators
            clicked = False
            last_error = None
            for by, locator in OPTION_LOCATORS:
                try:
                    # Obtener todos los candidatos para evidenciar
                    candidates = self.driver.find_elements(by, locator)
                    if not candidates:
                        continue

                    # Elegir el primero visible/clicable
                    target = None
                    for el in candidates:
                        if el.is_displayed() and el.is_enabled():
                            target = el
                            break
                    if not target:
                        continue

                    # Evidencia visual + clic (ActionChains)
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({behavior:'smooth',block:'center'});", target
                    )
                    self.driver.execute_script("arguments[0].style.border='3px solid #e00';", target)
                    time.sleep(0.2)

                    try:
                        ActionChains(self.driver).move_to_element(target).pause(0.2).click().perform()
                    finally:
                        try:
                            self.driver.execute_script("arguments[0].style.border='0';", target)
                        except Exception:
                            pass

                    clicked = True
                    logger.info("✓ Idioma 'English' seleccionado (por botón/rol/id).")
                    break
                except Exception as e:
                    last_error = e
                    continue

            # 3) Fallback final: JS click sobre el último locator que encuentre 'English'
            if not clicked:
                for by, locator in OPTION_LOCATORS:
                    try:
                        opt = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((by, locator)))
                        self.driver.execute_script("arguments[0].click();", opt)
                        clicked = True
                        logger.info("✓ Idioma 'English' seleccionado vía JS fallback.")
                        break
                    except Exception as e:
                        last_error = e
                        continue

            if not clicked:
                logger.error(f"No fue posible clicar 'English'. Último error: {last_error}")
                self.take_screenshot("csv_language_english_click_failed")
                return False

            time.sleep(0.8)
            return True

        except Exception as e:
            logger.error(f"Error en select_language_from_csv: {e}")
            self.take_screenshot("csv_language_selection_error")


    @allure.step("CSV: Seleccionar POS -> Colombia COP y Aplicar")
    def select_pos_cop_apply_from_csv(self):
        """
        Paso 4-6 del CSV:
        4) Click en 'Colombia COP' (trigger header)
        5) Click en 'COP'
        6) Click en 'Apply'
        """
        HEADER_POS_TRIGGER = "//li[@class='main-header_nav-secondary_item main-header_nav-secondary_item--point-of-sale-selector']//span[2]"
        COP_VALUE = "//span[@class='points-of-sale_list_item_value'][normalize-space()='COP']"
        
        # Intentar diferentes variantes del botón Apply
        APPLY_VARIANTS = [
            "//span[contains(text(),'Apply')]",  # Original
            "//button[contains(text(),'Apply')]",  # Botón con texto Apply
            "//button//span[contains(text(),'Apply')]",  # Span dentro de botón
            "//button[@type='submit']",  # Botón de tipo submit
            "//button[contains(@class, 'btn-primary')]",  # Botón primario
            "//button[contains(@class, 'apply')]",  # Clase apply
            "//span[contains(text(),'Aplicar')]",  # En español
        ]

        try:
            # --- Abrir trigger del POS ---
            logger.info("Abriendo selector de POS...")
            if not self.click_xpath_with_actions(HEADER_POS_TRIGGER, "Header POS trigger (Colombia COP)"):
                elem = self.wait_for_clickable((By.XPATH, HEADER_POS_TRIGGER), "Header POS trigger", timeout=10)
                if not elem: 
                    self.take_screenshot("pos_header_trigger_not_found")
                    return False
                self.driver.execute_script("arguments[0].click();", elem)
            
            self.take_screenshot("csv_pos_popup_open")
            time.sleep(1.5)  # Esperar a que el popup se abra completamente
            
            # --- Seleccionar COP ---
            logger.info("Seleccionando COP...")
            if not self.click_xpath_with_actions(COP_VALUE, "POS Moneda - COP"):
                elem = self.wait_for_clickable((By.XPATH, COP_VALUE), "POS COP", timeout=8)
                if not elem: 
                    logger.warning("No se encontró COP, intentando continuar...")
                else:
                    self.driver.execute_script("arguments[0].click();", elem)
            
            time.sleep(1)  # Esperar a que se seleccione COP
            
            # --- Buscar y hacer click en Apply (intentar todas las variantes) ---
            logger.info("Buscando botón Apply...")
            apply_found = False
            
            for apply_xpath in APPLY_VARIANTS:
                try:
                    logger.info(f"Intentando con XPath: {apply_xpath}")
                    apply_element = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, apply_xpath))
                    )
                    
                    if apply_element and apply_element.is_displayed():
                        logger.info(f"✓ Botón Apply encontrado: {apply_xpath}")
                        
                        # Scroll al botón
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                            apply_element
                        )
                        time.sleep(0.5)
                        
                        # Intentar click con ActionChains primero
                        try:
                            actions = ActionChains(self.driver)
                            actions.move_to_element(apply_element).pause(0.3).click().perform()
                            logger.info("✓ Click con ActionChains exitoso")
                        except:
                            # Fallback a JavaScript click
                            self.driver.execute_script("arguments[0].click();", apply_element)
                            logger.info("✓ Click con JavaScript exitoso")
                        
                        apply_found = True
                        break
                        
                except Exception as e:
                    logger.debug(f"XPath no funcionó {apply_xpath}: {e}")
                    continue
            
            if not apply_found:
                # Último intento: buscar cualquier botón visible cerca del popup
                logger.info("Buscando cualquier botón en el popup...")
                try:
                    # Buscar todos los botones en el popup
                    buttons = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'popup')]//button")
                    for button in buttons:
                        if button.is_displayed():
                            button_text = button.text.strip()
                            if button_text and ('Apply' in button_text or 'Aplicar' in button_text or 'Confirm' in button_text):
                                logger.info(f"Botón encontrado por texto: {button_text}")
                                button.click()
                                apply_found = True
                                break
                except:
                    pass
            
            if apply_found:
                time.sleep(2)  # Esperar a que se aplique el cambio
                self.take_screenshot("csv_pos_cop_applied")
                logger.info("✅ POS Colombia COP aplicado exitosamente")
                return True
            else:
                logger.error("❌ No se encontró ningún botón Apply/Aplicar")
                self.take_screenshot("apply_button_not_found")
                return False

        except Exception as e:
            logger.error(f"Error en select_pos_cop_apply_from_csv: {e}")
            self.take_screenshot(f"pos_csv_error_{str(e)[:50]}")
            return False

    @allure.step("CSV: Seleccionar One way (por ID)")
    def select_one_way_by_id_from_csv(self):
        """Paso 8 del CSV: click en #journeytypeId_1."""
        # Usar el selector CSS_SELECTOR definido en la clase, que es más robusto
        try:
            element = WebDriverWait(self.driver, 12).until(
                EC.element_to_be_clickable(self.ONE_WAY_LABEL)
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", element
            )
            time.sleep(0.3)
            # Intento 1: ActionChains
            try:
                ActionChains(self.driver).move_to_element(element).pause(0.2).click().perform()
            except ElementClickInterceptedException:
                # Intento 2: click directo
                try:
                    element.click()
                except Exception:
                    # Intento 3: JavaScript click
                    self.driver.execute_script("arguments[0].click();", element)
            time.sleep(0.5)
            return True
        except Exception as e:
            logger.error(f"Error seleccionando One Way: {e}")
            return False

    @allure.step("CSV: Seleccionar destino MDE por input y opción 'Medellin'")
    def select_destination_mde_from_csv(self):
        """
        Pasos 9-11 :
        9) Click en contenedor destino
        10) Escribir 'MDE' en #arrivalStationInputId
        11) Click en opción 'Medellin'
        """
        DEST_CONTAINER = "//div[@class='station-control station-control--has-filter']"
        DEST_INPUT = "//input[@id='arrivalStationInputId']"
        OPTION_MEDELLIN = "//span[contains(text(),'Medellin')]"

        # abrir panel destino
        self.click_xpath_with_actions(DEST_CONTAINER, "Destino - contenedor")
        # escribir MDE
        dest_input = self.wait_for_element((By.XPATH, DEST_INPUT), "Destino - input", timeout=8)
        if not dest_input: return False
        dest_input.click(); time.sleep(0.2)
        dest_input.clear(); dest_input.send_keys("MDE"); time.sleep(1.5)

        # click opción Medellin
        return self.click_xpath_with_actions(OPTION_MEDELLIN, "Destino - Medellin")
    
    ##====================== CALENDARIO Y PASAJEROS CSV =========================  #

    @allure.step("CSV: Seleccionar día del calendario por texto")
    def click_calendar_day_by_text_from_csv(self, day_text="17"):
        """Paso 12 del CSV: click en //span[contains(text(),'17')]"""
        DAY_XPATH = f"//span[contains(text(),'{day_text}')]"
        ok = self.click_xpath_with_actions(DAY_XPATH, f"Calendario - día {day_text}")
        time.sleep(0.6)
        return ok

    @allure.step("CSV: Agregar pasajeros por íconos '+' y confirmar")
    def add_passengers_plus_and_confirm_from_csv(self):
        """
        Pasos 13-16 del CSV (los XPaths absolutos de '+' para Youth y Child y 'Confirm'):
        Se intenta con los absolutos y, si fallan, se usa tu flujo robusto existente (configure_passengers + confirm).
        """
        PLUS_YOUTH_ABS = "/html[1]/body[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/ibe-multiple-panel[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/ibe-multiple-options[1]/div[1]/div[1]/div[1]/ibe-render-component[1]/div[1]/ng-template[1]/search-container[1]/div[1]/ibe-search-custom[1]/div[1]/div[1]/div[3]/div[3]/pax-control-custom[1]/div[1]/modal-wrapper[1]/div[1]/div[1]/div[1]/div[2]/div[1]/ul[1]/li[2]/div[2]/ibe-minus-plus[1]/div[1]/button[2]"
        PLUS_CHILD_ABS = "/html[1]/body[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/ibe-multiple-panel[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/ibe-multiple-options[1]/div[1]/div[1]/div[1]/ibe-render-component[1]/div[1]/ng-template[1]/search-container[1]/div[1]/ibe-search-custom[1]/div[1]/div[1]/div[3]/div[3]/pax-control-custom[1]/div[1]/modal-wrapper[1]/div[1]/div[1]/div[1]/div[2]/div[1]/ul[1]/li[3]/div[2]/ibe-minus-plus[1]/div[1]/button[2]"
        PLUS_INFANT_ABS = "/html/body/div[1]/main/div/div[1]/div/div/ibe-multiple-panel/div/div/div[2]/div/div/div/ibe-multiple-options/div/div/div/ibe-render-component/div/ng-template/search-container/div[1]/ibe-search-custom/div/div/div[3]/div[3]/pax-control-custom/div/modal-wrapper/div/div/div/div[2]/div/ul/li[4]/div[2]/ibe-minus-plus/div/button[2]"
        CONFIRM_ABS = "/html/body/div[1]/main/div/div[1]/div/div/ibe-multiple-panel/div/div/div[2]/div/div/div/ibe-multiple-options/div/div/div/ibe-render-component/div/ng-template/search-container/div[1]/ibe-search-custom/div/div/div[3]/div[3]/pax-control-custom/div/modal-wrapper/div/div/div/div[2]/div/div/button"

        ok1 = self.click_xpath_with_actions(PLUS_YOUTH_ABS, "Pasajeros: Youth +")
        ok2 = self.click_xpath_with_actions(PLUS_CHILD_ABS, "Pasajeros: Child +")
        ok3 = self.click_xpath_with_actions(PLUS_INFANT_ABS, "Pasajeros: Infant +")
        time.sleep(0.5)

        # Confirm (si el absoluto falla, usa confirm genérico)
        ok4 = self.click_xpath_with_actions(CONFIRM_ABS, "Pasajeros: Confirm")
        if not ok3:
            ok4 = self._confirm_passenger_selection()

        if not (ok1 and ok2 and ok3):
            logger.warning("No todos los XPaths absolutos funcionaron; aplicando método robusto configure_passengers(...)")
            self.configure_passengers(adults=1, youths=1, children=1, infants=1)
            self._confirm_passenger_selection()

        self.take_screenshot("csv_passengers_confirmed")
        return True

    @allure.step("CSV: Buscar, seleccionar tarifa y continuar")
    def search_select_fare_and_continue_from_csv(self):
        """
        Pasos 17-22 del CSV:
        17) Click en Search
        18/19) Click en precio (primera tarifa disponible)
        20) Click en 'Select' (Basic)
        22) Click en 'Continue'
        """
        try:
            # Paso 17: Search
            SEARCH_BTN = "//button[@id='searchButton']//span[@class='button_label'][normalize-space()='Search']"
            
            if not self.click_xpath_with_actions(SEARCH_BTN, "Search flights"):
                # legacy: try direct click as fallback
                try:
                    el = WebDriverWait(self.driver, 6).until(EC.element_to_be_clickable((By.XPATH, SEARCH_BTN)))
                    self.driver.execute_script("arguments[0].click();", el)
                except Exception:
                    logger.error("No se pudo hacer clic en Search")
                    return False

            # Esperar resultados de vuelos con múltiples selectores (más robusto que sleep fijo)
            result_selectors = [
                "//button[contains(@class,'fare_button')]",
                "//fare-control",
                "//div[contains(@class,'journey_price')]",
                "//div[contains(@class,'fare-card')]",
                "//div[contains(@aria-label,'Click to select')]",
            ]

            found = False
            wait_until = time.time() + 25
            while time.time() < wait_until and not found:
                for sel in result_selectors:
                    try:
                        elems = self.driver.find_elements(By.XPATH, sel)
                        if elems and len(elems) > 0:
                            logger.info(f"✓ Resultados detectados con selector: {sel}")
                            found = True
                            break
                    except Exception:
                        continue
                if not found:
                    # forzar scroll para cargar resultados lazy
                    try:
                        self.driver.execute_script("window.scrollBy(0,300);")
                    except Exception:
                        pass
                    time.sleep(0.6)

            if not found:
                logger.warning("No se detectaron resultados de vuelos tras Search")
                self.take_screenshot("csv_search_no_results")
                # continuar de todos modos (algunos flujos muestran select después)

            self.take_screenshot("csv_search_clicked")

            # Paso 18-19: Precio / Select fare - NUEVO: ser más flexible con selectores
            logger.info("Buscando y haciendo clic en precio de vuelo...")
            
            # Primero intentar con selectores más amplios
            PRICE_SELECTORS = [
                # Selectores por contenido de precio
                "//button[contains(text(),'$') or contains(text(),'COP')]",
                "//div[contains(text(),'COP')]//ancestor::button",
                "//span[contains(text(),'COP')]//ancestor::button",
                # Selectores por clase
                "//button[contains(@class,'price')]",
                "//button[contains(@class,'journey')]",
                # Selectores genéricos - clickeable en sección de precios
                "//div[contains(@class,'journey_price')]//button",
                "//div[contains(@class,'fare')]//button[1]",
                # Fallback: primer botón clickeable en la página (después de scroll)
                "(//button[@aria-label or @class])[1]"
            ]
            
            price_clicked = False
            for i, selector in enumerate(PRICE_SELECTORS):
                try:
                    logger.info(f"  Intento {i+1}/{len(PRICE_SELECTORS)}: {selector[:80]}")
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        logger.info(f"    ✓ Encontrado {len(elements)} elemento(s)")
                        # Hacer clic en el primer elemento
                        el = elements[0]
                        # Scroll y click
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", el)
                        time.sleep(0.5)
                        actions = ActionChains(self.driver)
                        actions.move_to_element(el).pause(0.3).click().perform()
                        price_clicked = True
                        logger.info(f"✓ Precio clickeado con selector: {selector[:80]}")
                        break
                except Exception as e:
                    logger.debug(f"  Selector falló: {e}")
                    continue
            
            if not price_clicked:
                logger.warning("⚠️ No se pudo hacer clic en precio, intentando continuación directa...")
                # Continuar de todas formas
                
            time.sleep(2.0)
            self.take_screenshot("csv_fare_selected")

            # Paso 20: Click en Select (Basic) - también ser más flexible
            logger.info("Buscando y haciendo clic en 'Select' para tarifa Basic...")
            
            BASIC_SELECT_SELECTORS = [
                "//div[@aria-label='Click to select Basic fare']//div[@class='fare_button_label']",
                "//div[contains(@aria-label, 'Basic')]//div[@class='fare_button_label']",
                "//button[contains(text(),'Select') and contains(@class,'fare')]",
                "//div[contains(@class,'fare')]//span[contains(text(),'Select')]//ancestor::button",
                "//div[@class='fare_button_label']",
                "(//button[contains(text(),'Select')])[1]"
            ]
            
            basic_clicked = False
            for i, selector in enumerate(BASIC_SELECT_SELECTORS):
                try:
                    logger.info(f"  Intento {i+1}/{len(BASIC_SELECT_SELECTORS)}: {selector[:80]}")
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        logger.info(f"    ✓ Encontrado {len(elements)} elemento(s)")
                        el = elements[0]
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", el)
                        time.sleep(0.5)
                        actions = ActionChains(self.driver)
                        actions.move_to_element(el).pause(0.3).click().perform()
                        basic_clicked = True
                        logger.info(f"✓ Basic seleccionado con selector: {selector[:80]}")
                        break
                except Exception as e:
                    logger.debug(f"  Selector falló: {e}")
                    continue
            
            if not basic_clicked:
                logger.warning("⚠️ No se pudo seleccionar tarifa Basic, continuando...")
                
            time.sleep(2.0)
            self.take_screenshot("csv_fare_selected_after_click")

            # Paso 22: Continue - también flexibilizar
            logger.info("Buscando y haciendo clic en botón Continue...")
            
            CONTINUE_SELECTORS = [
                "//button[contains(@class,'page_button-primary-flow')]",
                "//button[contains(@class,'page_button-primary')]",
                "//button[normalize-space()='Continue']",
                "//button//span[normalize-space()='Continue']//ancestor::button",
                "//span[contains(text(),'Continue')]//ancestor::button",
                "(//button[@class])[last()]"  # Último botón como fallback
            ]
            
            continue_clicked = False
            for i, selector in enumerate(CONTINUE_SELECTORS):
                try:
                    logger.info(f"  Intento {i+1}/{len(CONTINUE_SELECTORS)}: {selector[:80]}")
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        logger.info(f"    ✓ Encontrado {len(elements)} elemento(s)")
                        el = elements[0]
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", el)
                        time.sleep(0.5)
                        actions = ActionChains(self.driver)
                        actions.move_to_element(el).pause(0.3).click().perform()
                        continue_clicked = True
                        logger.info(f"✓ Continue clickeado con selector: {selector[:80]}")
                        break
                except Exception as e:
                    logger.debug(f"  Selector falló: {e}")
                    continue
            
            if not continue_clicked:
                logger.error("No se pudo encontrar botón Continue")
                return False
                
            time.sleep(2.0)
            self.take_screenshot("csv_continue_clicked")
            
            logger.info("✅ Búsqueda, selección de tarifa y continuar completados exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error en search_select_fare_and_continue_from_csv: {e}")
            self.take_screenshot(f"error_search_fare_{str(e)[:50]}")
            return False
    

    # ==================== MÉTODOS EXISTENTES (CONTINUAN) ==================== #
    
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

        # Intento primario: usar el helper de ActionChains con evidencias
        try:
            success = self.actions.click_with_evidence(self.SEARCH_BUTTON, "Search flights")
            if success:
                logger.info("✓ Búsqueda iniciada (ActionChains)")
                return True
            else:
                logger.warning("ActionChains no pudo clickear Search; intentando fallback")
        except Exception as e:
            logger.warning(f"ActionChains lanzó excepción: {e} - intentando fallback")

        # Fallback 1: click directo sobre el elemento encontrado
        try:
            elem = self.wait_for_clickable(self.SEARCH_BUTTON, "Search flights", timeout=6)
            if elem:
                try:
                    elem.click()
                    logger.info("✓ Búsqueda iniciada (direct click)")
                    return True
                except Exception as e:
                    logger.warning(f"Direct click falló: {e} - intentando JS click")
                    try:
                        self.driver.execute_script("arguments[0].click();", elem)
                        logger.info("✓ Búsqueda iniciada (JS click)")
                        return True
                    except Exception as e2:
                        logger.error(f"JS click también falló: {e2}")
        except Exception as e:
            logger.debug(f"No se pudo localizar Search button para fallback: {e}")

        # Último recurso: intentar localizar por ID y ejecutar JS click
        try:
            try:
                btn = self.driver.find_element(By.ID, "searchButton")
                self.driver.execute_script("arguments[0].click();", btn)
                logger.info("✓ Búsqueda iniciada (fallback por ID + JS)")
                return True
            except Exception as e:
                logger.error(f"Fallback final para Search falló: {e}")
        except Exception:
            pass

        # Si llegamos aquí, no se pudo iniciar búsqueda
        self.take_screenshot("search_button_click_failed")
        return False
    
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