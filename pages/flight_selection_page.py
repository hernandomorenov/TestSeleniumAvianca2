import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from pages.base_page import BasePage
from utils.logger import logger

class FlightSelectionPage(BasePage):
    """Página de selección de vuelos - MEJORADA CON ACTIONCHAINS"""
    
    # ==================== SELECTORES BASADOS EN CSV ====================
    
    # Paso 2: Select fare label
    SELECT_FARE_LABEL = (By.XPATH, "//div[@class='journey_price_fare-select_label ng-tns-c12-2 ng-star-inserted']")
    
    # Paso 4: Botón Select de tarifa Basic
    SELECT_BASIC_FARE_BUTTON = (By.XPATH, "//div[@aria-label='Click to select Basic fare']//div[@class='fare_button_label']")
    
    # Alternativas para tarifa Basic
    BASIC_FARE_CARD = (By.XPATH, "//div[contains(@aria-label, 'Basic fare')]")
    BASIC_FARE_CONTAINER = (By.XPATH, "//fare-control[contains(@class, 'basic') or contains(., 'Basic')]")
    
    # Primer botón Select disponible (fallback)
    FIRST_SELECT_BUTTON = (By.XPATH, "(//div[@class='fare_button_label'])[1]")
    
    # Paso 6: Botón Continue
    CONTINUE_BUTTON = (By.XPATH, "//button[@class='button page_button btn-action page_button-primary-flow ng-star-inserted']")
    
    # Selectores alternativos
    FARE_OPTION = (By.XPATH, "//div[contains(@class, 'fare-card')][1]")
    FARE_PRICE = (By.XPATH, "//div[contains(@class, 'fare-price')]")
    
    # ==================== MÉTODOS OPTIMIZADOS CON ACTIONCHAINS ====================
    
    @allure.step("Esperar a que cargue la página de selección de vuelos")
    def wait_for_page_load(self):
        """Esperar a que cargue la página de selección de vuelos"""
        logger.info("Esperando a que cargue la página de selección de vuelos...")
        try:
            # Esperar a que aparezca el label "Select fare"
            self.wait_for_element(self.SELECT_FARE_LABEL, timeout=20)
            logger.info("✓ Página de selección de vuelos cargada")
            time.sleep(2)  # Dar tiempo extra para animaciones
            return True
        except Exception as e:
            logger.error(f"Error cargando página de selección de vuelos: {e}")
            self.take_screenshot("flights_load_error")
            return False
    
    @allure.step("PASO 2: Click en Select fare label con ActionChains")
    def click_select_fare_label(self):
        """Click en el label 'Select fare' usando ActionChains"""
        logger.info("PASO 2: Click en Select fare label con ActionChains")
        
        try:
            select_fare_label = self.wait_for_element(self.SELECT_FARE_LABEL, timeout=10)
            
            if select_fare_label:
                # Scroll al elemento
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                    select_fare_label
                )
                time.sleep(1)
                
                # Usar ActionChains para hover y click
                actions = ActionChains(self.driver)
                actions.move_to_element(select_fare_label).pause(0.5).click().perform()
                
                logger.info("✓ Click en Select fare label realizado con ActionChains")
                time.sleep(1)
                return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Select fare label no accesible con ActionChains: {e}")
            return False
    
    @allure.step("PASO 3: Scroll down suave")
    def scroll_down_to_fares(self):
        """Scroll down para ver las tarifas"""
        logger.info("PASO 3: Scroll down para ver tarifas")
        
        try:
            # Scroll suave con ActionChains
            actions = ActionChains(self.driver)
            
            # Scroll gradual (más visible)
            for _ in range(3):
                actions.scroll_by_amount(0, 100).perform()
                time.sleep(0.3)
            
            logger.info("✓ Scroll down realizado")
            time.sleep(1)
            return True
            
        except Exception as e:
            # Fallback: JavaScript scroll
            self.driver.execute_script("window.scrollBy(0, 300);")
            logger.info("✓ Scroll down realizado (JavaScript)")
            time.sleep(1)
            return True
    
    @allure.step("PASO 4: Seleccionar tarifa Basic con ActionChains - DESTACADO")
    def select_basic_fare_with_actions(self):
        """
        Seleccionar tarifa Basic usando ActionChains para mejor visualización
        Hace hover sobre la tarifa antes de hacer click
        """
        logger.info("PASO 4: Seleccionando tarifa Basic con ActionChains (DESTACADO)")
        
        try:
            # Buscar botón de tarifa Basic (múltiples intentos)
            select_button = None
            
            # Intento 1: Selector específico de Basic
            try:
                select_button = self.wait_for_element(self.SELECT_BASIC_FARE_BUTTON, timeout=5)
                logger.info("✓ Botón Basic fare encontrado (selector específico)")
            except:
                pass
            
            # Intento 2: Por aria-label
            if not select_button:
                try:
                    select_button = self.wait_for_element(self.BASIC_FARE_CARD, timeout=5)
                    # Buscar el botón dentro de la card
                    if select_button:
                        buttons = select_button.find_elements(By.XPATH, ".//button | .//div[@class='fare_button_label']")
                        if buttons:
                            select_button = buttons[0]
                            logger.info("✓ Botón Basic fare encontrado (aria-label)")
                except:
                    pass
            
            # Intento 3: Primer Select disponible
            if not select_button:
                try:
                    select_button = self.wait_for_element(self.FIRST_SELECT_BUTTON, timeout=5)
                    logger.info("✓ Primer botón Select encontrado (fallback)")
                except:
                    logger.error("❌ No se encontró ningún botón Select")
                    return False
            
            if select_button:
                # Scroll al botón con comportamiento suave
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                    select_button
                )
                time.sleep(1)
                
                # ===== ACTIONCHAINS PARA DESTACAR LA SELECCIÓN =====
                actions = ActionChains(self.driver)
                
                # 1. Mover el mouse al botón (hover)
                logger.info("  → Moviendo cursor a tarifa Basic (hover)...")
                actions.move_to_element(select_button).perform()
                time.sleep(1)  # Pausa para que se vea el hover
                
                # 2. Resaltar el elemento con JavaScript (borde destacado)
                try:
                    original_style = select_button.get_attribute("style")
                    self.driver.execute_script(
                        "arguments[0].style.border = '3px solid #00FF00';"
                        "arguments[0].style.boxShadow = '0 0 10px #00FF00';",
                        select_button
                    )
                    logger.info("  → Tarifa Basic resaltada visualmente")
                    time.sleep(1)  # Pausa para que se vea el resaltado
                except:
                    pass
                
                # 3. Click con ActionChains
                logger.info("  → Haciendo click en tarifa Basic...")
                actions.click(select_button).perform()
                time.sleep(0.5)
                
                # 4. Restaurar estilo original (si se pudo cambiar)
                try:
                    if original_style:
                        self.driver.execute_script(
                            f"arguments[0].style = '{original_style}';",
                            select_button
                        )
                except:
                    pass
                
                logger.info("✅ Tarifa Basic seleccionada con ActionChains (DESTACADO)")
                self.take_screenshot("basic_fare_selected")
                time.sleep(2)
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error seleccionando tarifa con ActionChains: {e}")
            self.take_screenshot("fare_selection_error")
            return False
    
    @allure.step("PASO 5: Scroll up suave")
    def scroll_up_after_selection(self):
        """Scroll up después de seleccionar tarifa"""
        logger.info("PASO 5: Scroll up")
        
        try:
            # Scroll suave hacia arriba con ActionChains
            actions = ActionChains(self.driver)
            
            # Scroll gradual (más visible)
            for _ in range(2):
                actions.scroll_by_amount(0, -100).perform()
                time.sleep(0.3)
            
            logger.info("✓ Scroll up realizado")
            time.sleep(1)
            return True
            
        except Exception as e:
            # Fallback: JavaScript scroll
            self.driver.execute_script("window.scrollBy(0, -200);")
            logger.info("✓ Scroll up realizado (JavaScript)")
            time.sleep(1)
            return True
    
    @allure.step("Seleccionar tarifa Basic - FLUJO COMPLETO CON ACTIONCHAINS")
    def select_fare(self, fare_type="Basic"):
        """
        Seleccionar tarifa usando los pasos del CSV con ActionChains
        
        Pasos del CSV:
        2. Click on "Select fare" label (con ActionChains)
        3. Scroll down (con ActionChains)
        4. Click on "Select" button Basic (con ActionChains + destacado visual)
        5. Scroll up (con ActionChains)
        """
        logger.info(f"Seleccionando tarifa {fare_type} con ActionChains (CSV)...")
        logger.info("="*60)
        
        success = True
        
        # PASO 2: Click en label (opcional)
        if not self.click_select_fare_label():
            logger.warning("⚠️ Select fare label no disponible, continuando...")
        
        # PASO 3: Scroll down
        self.scroll_down_to_fares()
        
        # PASO 4: Seleccionar tarifa Basic con ActionChains (DESTACADO)
        if not self.select_basic_fare_with_actions():
            logger.error("❌ No se pudo seleccionar tarifa Basic")
            success = False
        
        # PASO 5: Scroll up
        self.scroll_up_after_selection()
        
        logger.info("="*60)
        logger.info(f"{'✅ Tarifa seleccionada correctamente' if success else '❌ Error seleccionando tarifa'}")
        
        return success
    
    @allure.step("Verificar precio del vuelo")
    def verify_flight_price(self):
        """Verificar y obtener el precio del vuelo"""
        logger.info("Verificando precio del vuelo...")
        try:
            price_element = self.wait_for_element(self.FARE_PRICE, timeout=10)
            if price_element:
                price_text = price_element.text.strip()
                
                if price_text:
                    logger.info(f"✓ Precio encontrado: {price_text}")
                    return price_text
            
            logger.warning("No se encontró texto de precio")
            return None
            
        except Exception as e:
            logger.debug(f"No se pudo verificar precio: {e}")
            return None
    
    @allure.step("PASO 6: Continuar a página de pasajeros con ActionChains")
    def continue_to_passengers(self):
        """
        Hacer clic en el botón Continue para ir a pasajeros
        Paso 6 del CSV: Click on "Continue step" con ActionChains
        """
        logger.info("PASO 6: Click en Continue button con ActionChains")
        
        try:
            # Buscar botón Continue
            continue_button = self.wait_for_element(self.CONTINUE_BUTTON, timeout=10)
            
            if not continue_button:
                logger.error("❌ Botón Continue no encontrado")
                return False
            
            # Hacer scroll al botón
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                continue_button
            )
            time.sleep(1)
            
            # Usar ActionChains para hover y click
            actions = ActionChains(self.driver)
            
            # Hover sobre el botón
            logger.info("  → Moviendo cursor a botón Continue...")
            actions.move_to_element(continue_button).pause(0.5).perform()
            time.sleep(0.5)
            
            # Click con ActionChains
            logger.info("  → Haciendo click en Continue...")
            actions.click(continue_button).perform()
            
            logger.info("✅ Continue button clicked con ActionChains - Navegando a pasajeros")
            
            # Esperar a que se procese
            time.sleep(3)
            return True
            
        except Exception as e:
            logger.warning(f"Error con ActionChains, intentando JavaScript: {e}")
            
            # Fallback: JavaScript click
            try:
                continue_button = self.wait_for_element(self.CONTINUE_BUTTON, timeout=5)
                self.driver.execute_script("arguments[0].click();", continue_button)
                logger.info("✓ Continue button clicked (JavaScript fallback)")
                time.sleep(3)
                return True
            except:
                logger.error("❌ No se pudo hacer click en Continue")
                self.take_screenshot("continue_error")
                return False
    
    @allure.step("Seleccionar tarifa y continuar - FLUJO COMPLETO CSV CON ACTIONCHAINS")
    def select_fare_and_continue(self, fare_type="Basic"):
        """
        Flujo completo basado en CSV con ActionChains:
        1. Esperar carga de página
        2-5. Seleccionar tarifa con ActionChains (DESTACADO)
        6. Continuar con ActionChains
        """
        logger.info("="*80)
        logger.info("INICIANDO FLUJO COMPLETO DE FLIGHT SELECTION CON ACTIONCHAINS")
        logger.info("="*80)
        
        success = True
        
        # Paso 1: Esperar carga
        if not self.wait_for_page_load():
            logger.error("❌ Página no cargó")
            return False
        
        # Pasos 2-5: Seleccionar tarifa con ActionChains
        if not self.select_fare(fare_type):
            logger.error("❌ No se pudo seleccionar tarifa")
            success = False
        
        # Verificar precio (opcional)
        price = self.verify_flight_price()
        if price:
            logger.info(f"ℹ️  Precio del vuelo: {price}")
        
        # Paso 6: Continuar con ActionChains
        if not self.continue_to_passengers():
            logger.error("❌ No se pudo continuar a pasajeros")
            return False
        
        logger.info("="*80)
        logger.info(f"{'✅ FLIGHT SELECTION COMPLETADO' if success else '⚠️  FLIGHT SELECTION CON WARNINGS'}")
        logger.info("="*80)
        
        return success
    
    @allure.step("Método alternativo: Seleccionar tarifa con máxima visibilidad")
    def select_fare_with_highlight(self, fare_type="Basic"):
        """
        Método alternativo que hace MUY VISIBLE la selección
        Resalta, hace hover, pausa, y click
        """
        logger.info(f"🎯 Seleccionando tarifa {fare_type} con MÁXIMA VISIBILIDAD")
        
        try:
            # Buscar tarifa Basic
            select_button = None
            
            for selector in [self.SELECT_BASIC_FARE_BUTTON, self.FIRST_SELECT_BUTTON]:
                try:
                    select_button = self.wait_for_element(selector, timeout=5)
                    if select_button:
                        break
                except:
                    continue
            
            if not select_button:
                logger.error("❌ No se encontró botón de tarifa")
                return False
            
            # Scroll
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                select_button
            )
            time.sleep(1)
            
            # 1. Resaltar con animación
            logger.info("  🎨 Resaltando tarifa Basic...")
            self.driver.execute_script("""
                arguments[0].style.border = '5px solid #FF0000';
                arguments[0].style.boxShadow = '0 0 20px #FF0000';
                arguments[0].style.backgroundColor = 'rgba(255, 255, 0, 0.3)';
                arguments[0].style.transition = 'all 0.5s';
            """, select_button)
            time.sleep(2)  # Pausa larga para ver el resaltado
            
            # 2. Hover con ActionChains
            logger.info("  👆 Hover sobre tarifa Basic...")
            actions = ActionChains(self.driver)
            actions.move_to_element(select_button).pause(1).perform()
            time.sleep(1)
            
            # 3. Click
            logger.info("  🖱️  Click en tarifa Basic...")
            actions.click(select_button).perform()
            time.sleep(1)
            
            # 4. Restaurar estilo
            self.driver.execute_script("""
                arguments[0].style.border = '';
                arguments[0].style.boxShadow = '';
                arguments[0].style.backgroundColor = '';
            """, select_button)
            
            logger.info("✅ Tarifa seleccionada con MÁXIMA VISIBILIDAD")
            self.take_screenshot("basic_fare_highlighted")
            return True
            
        except Exception as e:
            logger.error(f"Error en selección con highlight: {e}")
            return False