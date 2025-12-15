import time
import os
from datetime import datetime
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
    
    # Paso 6: Botón Continue - Múltiples selectores por si la estructura cambia
    CONTINUE_BUTTON = (By.XPATH, "//button[@class='button page_button btn-action page_button-primary-flow ng-star-inserted']")
    CONTINUE_BUTTON_ALT1 = (By.XPATH, "//*[@id='maincontent']//button-container//button")
    CONTINUE_BUTTON_ALT2 = (By.XPATH, "//button-container//button[contains(@class, 'button-primary')]")
    CONTINUE_BUTTON_ALT3 = (By.CSS_SELECTOR, "button.page_button-primary-flow")
    CONTINUE_BUTTON_ALT4 = (By.XPATH, "//button[contains(@class, 'page_button-primary-flow')]//span[contains(text(), 'Continue')]/..")
    
    # Selectores alternativos
    FARE_OPTION = (By.XPATH, "//div[contains(@class, 'fare-card')][1]")
    FARE_PRICE = (By.XPATH, "//div[contains(@class, 'fare-price')]")
    
    # ==================== MÉTODOS OPTIMIZADOS CON ACTIONCHAINS ====================
    
    # @allure.step("Esperar a que cargue la página de selección de vuelos")
    # def wait_for_page_load(self):
    #     """Esperar a que cargue la página de selección de vuelos"""
    #     logger.info("Esperando a que cargue la página de selección de vuelos...")
    #     try:
    #         # Esperar a que aparezca el label "Select fare"
    #         self.wait_for_element(self.SELECT_FARE_LABEL, timeout=20)
    #         logger.info("✓ Página de selección de vuelos cargada")
    #         time.sleep(2)  # Dar tiempo extra para animaciones
    #         return True
    #     except Exception as e:
    #         logger.error(f"Error cargando página de selección de vuelos: {e}")
    #         self.take_screenshot("flights_load_error")
    #         return False
    @allure.step("Esperar carga de Vuelos")
    def wait_for_page_load(self):
        """
        Espera robusta a que carguen los resultados de vuelos.
        Intenta múltiples selectores que representen resultados/fare buttons
        y espera hasta un timeout total. Devuelve True si detecta alguno.
        """
        selectors = [
            "//button[contains(@class, 'fare_button')]",
            "//fare-control",
            "//div[contains(@class,'journey_price')]",
            "//div[contains(@class,'fare-card')]",
            "//div[contains(@aria-label,'Click to select')]",
            "//div[contains(@class,'journey') and contains(., 'Select')]",
            "//button[contains(., 'Select')]",
        ]

        end_time = time.time() + 25
        found = False
        while time.time() < end_time:
            for xpath in selectors:
                try:
                    elems = self.driver.find_elements(By.XPATH, xpath)
                    if elems and len(elems) > 0:
                        logger.info(f"✓ Resultados de vuelos detectados usando: {xpath}")
                        time.sleep(1.2)
                        return True
                except Exception:
                    continue

            # pequeño scroll para forzar carga lazy
            try:
                self.driver.execute_script("window.scrollBy(0, 250);")
            except Exception:
                pass
            time.sleep(0.6)

        logger.warning("No se detectaron resultados de vuelos en el tiempo esperado")
        self.take_screenshot("flights_no_results")
        # Dump HTML de contenedores relevantes para depuración
        try:
            self.dump_flight_results_html(prefix="no_results")
        except Exception:
            logger.debug("No se pudo volcar HTML de resultados")
        return False

    @allure.step("Volcar HTML de resultados de vuelos para depuración")
    def dump_flight_results_html(self, prefix: str = "dump"):
        """
        Extrae outerHTML de los contenedores candidatos de resultados de vuelo
        y lo guarda en `reports/flight_results_{prefix}_{timestamp}.txt`.
        Esto ayuda a ajustar XPaths cuando los selectores CSV no coinciden.
        """
        logger.info("Volcando HTML de resultados de vuelos para depuración...")
        try:
            # Selectores candidatos para volcar
            candidate_xpaths = [
                "//div[contains(@class,'journey')]",
                "//div[contains(@class,'journey_price')]",
                "//fare-control",
                "//div[contains(@class,'fare-card')]",
                "//div[contains(@class,'fare')]",
            ]

            os.makedirs(os.path.join(self.driver.current_url.split('://')[-1].split('/')[0] if False else "reports"), exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = os.path.join("reports", f"flight_results_{prefix}_{timestamp}.txt")

            with open(out_path, "w", encoding="utf-8") as fh:
                fh.write(f"URL: {self.driver.current_url}\n\n")
                for xpath in candidate_xpaths:
                    try:
                        elems = self.driver.find_elements(By.XPATH, xpath)
                        fh.write(f"\n--- XPath: {xpath} (found={len(elems)}) ---\n")
                        for i, el in enumerate(elems[:5]):
                            try:
                                outer = el.get_attribute('outerHTML')
                                fh.write(f"\n--- Element {i} outerHTML ---\n")
                                fh.write(outer[:5000] + ("\n... (truncated)\n" if outer and len(outer) > 5000 else "\n"))
                            except Exception as e:
                                fh.write(f"Error extrayendo outerHTML: {e}\n")
                    except Exception as e:
                        fh.write(f"Error buscando xpath {xpath}: {e}\n")

            logger.info(f"HTML de resultados volcado en: {out_path}")
            # También adjuntar al reporte Allure si está disponible
            try:
                with open(out_path, 'r', encoding='utf-8') as f:
                    allure.attach(f.read(), name=f"flight_results_{prefix}", attachment_type=allure.attachment_type.TEXT)
            except Exception:
                pass
            return out_path
        except Exception as e:
            logger.error(f"Error volcando HTML de resultados: {e}")
            return None
    @allure.step("Seleccionar tarifa CSV: {fare_name} para leg {leg_index}")
    def select_fare_smart(self, fare_name, leg_index=0):
        """
        Intenta seleccionar la tarifa usando la lógica exacta del CSV.
        
        CSV Step 23 (Ida/Basic): //div[@aria-label='Click to select Basic fare']//button[@class='fare_button']
        CSV Step 27 (Vuelta/Flex): //div[@aria-label='Click to select Flex fare']//div[@class='fare_button_label']
        """
        logger.info(f"Intentando seleccionar {fare_name} para el tramo {leg_index}")
        
        # 1. Definir los XPaths exactos del CSV según el nombre de la tarifa
        xpath_target = ""
        
        if "Basic" in fare_name:
            # XPath exacto del CSV línea 23
            xpath_target = "//div[@aria-label='Click to select Basic fare']//button[@class='fare_button']"
        elif "Flex" in fare_name:
            # XPath exacto del CSV línea 27 (nota que apunta al DIV interno, no al botón)
            xpath_target = "//div[@aria-label='Click to select Flex fare']//div[@class='fare_button_label']"
        else:
            # Fallback genérico
            xpath_target = f"//div[contains(@aria-label, '{fare_name}')]//button"

        try:
            # 2. Buscar TODOS los elementos que coincidan
            elements = self.driver.find_elements(By.XPATH, xpath_target)
            
            if not elements:
                logger.warning(f"No se encontraron elementos con {xpath_target}")
                return False

            # 3. Seleccionar el correcto basado en leg_index
            # Si hay 2 vuelos (Ida y Vuelta), elements debería tener al menos 2 botones si la tarifa existe en ambos.
            # Sin embargo, a veces el DOM cambia dinámicamente.
            
            target_el = None
            
            if leg_index < len(elements):
                target_el = elements[leg_index]
            else:
                # Si pedimos leg 1 (vuelta) pero solo hallamos 1 elemento, quizás es porque
                # el xpath es único para ese bloque. Intentamos el último disponible.
                target_el = elements[-1]

            # 4. Scroll y Click Robusto (JS)
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", target_el)
            time.sleep(1) # Esperar al scroll
            
            # Intentar click JS (es lo que mejor funciona en Avianca para evitar intercepciones)
            self.driver.execute_script("arguments[0].click();", target_el)
            logger.info(f"✅ Click JS exitoso en {fare_name} (Leg {leg_index})")
            time.sleep(2) # Esperar reacción de la página
            return True

        except Exception as e:
            logger.error(f"❌ Error seleccionando {fare_name}: {e}")
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
    
    # @allure.step("PASO 6: Continuar a página de pasajeros con ActionChains")
    # def continue_to_passengers(self):
    #     """
    #     Hacer clic en el botón Continue para ir a pasajeros
    #     Paso 6 del CSV: Click on "Continue step" con ActionChains
    #     Usa múltiples selectores por si la estructura HTML varía
    #     """
    #     logger.info("PASO 6: Click en Continue button con ActionChains")
        
    #     try:
    #         # Lista de selectores a intentar en orden
    #         continue_selectors = [
    #             self.CONTINUE_BUTTON,
    #             self.CONTINUE_BUTTON_ALT1,
    #             self.CONTINUE_BUTTON_ALT2,
    #             self.CONTINUE_BUTTON_ALT3,
    #             self.CONTINUE_BUTTON_ALT4,
    #         ]
            
    #         continue_button = None
            
    #         # Intentar cada selector hasta encontrar el botón
    #         for i, selector in enumerate(continue_selectors):
    #             try:
    #                 logger.info(f"  Intentando selector {i+1}/5...")
    #                 continue_button = self.wait_for_element(selector, timeout=5)
    #                 if continue_button:
    #                     logger.info(f"✓ Botón Continue encontrado con selector {i+1}")
    #                     break
    #             except Exception as e:
    #                 logger.debug(f"  Selector {i+1} no funcionó: {e}")
    #                 continue
            
    #         if not continue_button:
    #             logger.error("❌ Botón Continue no encontrado con ningún selector")
    #             self.take_screenshot("flight_continue_not_found")
    #             return False
            
    #         # Hacer scroll al botón
    #         self.driver.execute_script(
    #             "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
    #             continue_button
    #         )
    #         time.sleep(1)
            
    #         # Usar ActionChains para hover y click
    #         actions = ActionChains(self.driver)
            
    #         # Hover sobre el botón
    #         logger.info("  → Moviendo cursor a botón Continue...")
    #         actions.move_to_element(continue_button).pause(0.5).perform()
    #         time.sleep(0.5)
            
    #         # Click con ActionChains
    #         logger.info("  → Haciendo click en Continue...")
    #         actions.click(continue_button).perform()
            
    #         logger.info("✅ Continue button clicked con ActionChains - Navegando a pasajeros")
    #         self.take_screenshot("flight_continue_clicked")
            
    #         # Esperar a que se procese
    #         time.sleep(3)
    #         return True
            
    #     except Exception as e:
    #         logger.warning(f"Error con ActionChains, intentando JavaScript: {e}")
            
    #         # Fallback: JavaScript click con múltiples selectores
    #         try:
    #             for selector in [self.CONTINUE_BUTTON, self.CONTINUE_BUTTON_ALT1, self.CONTINUE_BUTTON_ALT2]:
    #                 try:
    #                     continue_button = self.wait_for_element(selector, timeout=3)
    #                     if continue_button:
    #                         self.driver.execute_script("arguments[0].click();", continue_button)
    #                         logger.info("✓ Continue button clicked (JavaScript fallback)")
    #                         time.sleep(3)
    #                         return True
    #                 except:
    #                     continue
                
    #             logger.error("❌ No se pudo hacer click en Continue con JavaScript")
    #             return False
                
    #         except Exception as e2:
    #             logger.error(f"❌ Error en fallback: {e2}")
    #             self.take_screenshot("flight_continue_error")
    #             return False
    #         except:
    #             logger.error("❌ No se pudo hacer click en Continue")
    #             self.take_screenshot("continue_error")
    #             return False
    @allure.step("Continuar a Pasajeros")
    def continue_to_passengers(self):
        # XPath exacto del CSV línea 30
        xpath_csv = "//button[contains(@class,'page_button-primary-flow')]//span[@class='button_label'][normalize-space()='Continue']"
        try:
            btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_csv)))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn)
            time.sleep(0.5)
            btn.click()
            return True
        except Exception:
            # Fallback JS
            try:
                self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.XPATH, xpath_csv))
                return True
            except:
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

    @allure.step("Seleccionar tarifa por tipo y por tramo (ida/vuelta)")
    def select_fare_for_leg(self, fare_type: str, leg_index: int = 0):
        """
        Selecciona una tarifa (Basic/Flex) para un tramo específico (ida=0, vuelta=1).
        Basado en los pasos exactos del CSV:
        - Busca la tarifa por aria-label o contenido textual
        - Hace clic en el botón 'Select' de esa tarifa
        """
        logger.info(f"🔍 Seleccionando tarifa '{fare_type}' para tramo {leg_index} (ida/vuelta)...")
        
        try:
            # PASO 1: Hacer scroll para ver la tarifa
            logger.info(f"  → Scroll down para visualizar tarifa '{fare_type}'...")
            self.driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(1.5)
            
            # PASO 2: Buscar el botón de tarifa usando múltiples estrategias
            # Estrategia 1: Buscar por aria-label exact (del CSV)
            xpath_by_aria = f"//div[@aria-label='Click to select {fare_type} fare']//button[@class='fare_button']"
            
            # Estrategia 2: Buscar por aria-label flexible
            xpath_by_aria_flex = f"//div[contains(@aria-label, '{fare_type}')]//button | //div[contains(@aria-label, '{fare_type}')]//span[@class='button_label']//ancestor::button"
            
            # Estrategia 3: Buscar fare-control y buscar Select dentro
            xpath_by_fare_control = f"//fare-control[contains(., '{fare_type}')]//button[contains(., 'Select') or contains(@class, 'fare_button')]"
            
            # Estrategia 4: Buscar todas las tarifas y usar índice
            xpath_all_fares = f"//fare-control | //div[contains(@class, 'fare-card')] | //div[contains(@class, 'fare_')]"
            
            select_button = None
            
            # Intentar estrategia 1
            logger.info(f"  Intento 1: Buscando por aria-label exacto...")
            try:
                select_button = self.wait_for_element((By.XPATH, xpath_by_aria), timeout=5)
                logger.info(f"  ✓ Encontrado por aria-label exacto")
            except Exception as e:
                logger.debug(f"    No encontrado: {e}")
            
            # Intentar estrategia 2
            if not select_button:
                logger.info(f"  Intento 2: Buscando por aria-label flexible...")
                try:
                    elements = self.driver.find_elements(By.XPATH, xpath_by_aria_flex)
                    if elements:
                        select_button = elements[min(leg_index, len(elements)-1)]
                        logger.info(f"  ✓ Encontrado por aria-label flexible (encontrados {len(elements)})")
                except Exception as e:
                    logger.debug(f"    No encontrado: {e}")
            
            # Intentar estrategia 3
            if not select_button:
                logger.info(f"  Intento 3: Buscando por fare-control...")
                try:
                    fare_controls = self.driver.find_elements(By.XPATH, xpath_by_fare_control)
                    if fare_controls:
                        select_button = fare_controls[min(leg_index, len(fare_controls)-1)]
                        logger.info(f"  ✓ Encontrado por fare-control (encontrados {len(fare_controls)})")
                except Exception as e:
                    logger.debug(f"    No encontrado: {e}")
            
            # Intento 4: Buscar todas las tarifas y filtrar por texto
            if not select_button:
                logger.info(f"  Intento 4: Buscando todas las tarifas y filtrando por texto...")
                try:
                    all_fare_elements = self.driver.find_elements(By.XPATH, xpath_all_fares)
                    logger.info(f"    Encontrados {len(all_fare_elements)} elementos de tarifa total")
                    
                    # Filtrar por contenido textual que contenga el tipo de tarifa
                    matching_fares = []
                    for elem in all_fare_elements:
                        try:
                            text = elem.text.upper()
                            if fare_type.upper() in text:
                                matching_fares.append(elem)
                                logger.debug(f"      → Tarifa con '{fare_type}' encontrada")
                        except:
                            pass
                    
                    if matching_fares:
                        # Seleccionar la correspondiente al leg_index
                        target_fare = matching_fares[min(leg_index, len(matching_fares)-1)]
                        
                        # Buscar el botón "Select" dentro de esta tarifa
                        buttons = target_fare.find_elements(By.XPATH, ".//button | .//span[@class='button_label']//ancestor::button")
                        if buttons:
                            select_button = buttons[0]
                            logger.info(f"  ✓ Encontrado botón Select dentro de tarifa '{fare_type}'")
                except Exception as e:
                    logger.debug(f"    No encontrado: {e}")
            
            # Último fallback: buscar cualquier botón "Select" que coincida con la posición
            if not select_button:
                logger.info(f"  Intento 5: Fallback - buscar botón Select por posición...")
                try:
                    all_select_buttons = self.driver.find_elements(By.XPATH, "//button[contains(., 'Select') or contains(., 'Seleccionar')]")
                    if all_select_buttons and len(all_select_buttons) > leg_index:
                        select_button = all_select_buttons[leg_index]
                        logger.info(f"  ✓ Encontrado Select button en posición {leg_index}")
                except Exception as e:
                    logger.debug(f"    No encontrado: {e}")
            
            if not select_button:
                logger.error(f"❌ No se encontró botón para seleccionar tarifa '{fare_type}' (tramo {leg_index})")
                self.take_screenshot(f"error_select_{fare_type}_leg_{leg_index}")
                try:
                    self.dump_flight_results_html(prefix=f"error_select_{fare_type}_leg_{leg_index}")
                except Exception:
                    logger.debug("No se pudo volcar HTML tras fallo de selección")
                return False
            
            # PASO 3: Hacer scroll al botón y clickearlo
            logger.info(f"  → Scrolling al botón Select...")
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", select_button)
            time.sleep(0.8)
            
            # Click con ActionChains (más confiable)
            logger.info(f"  → Haciendo click en Select button...")
            actions = ActionChains(self.driver)
            actions.move_to_element(select_button).pause(0.3).click().perform()
            time.sleep(1.0)
            
            logger.info(f"✅ Tarifa '{fare_type}' seleccionada exitosamente (tramo {leg_index})")
            self.take_screenshot(f"selected_{fare_type}_leg_{leg_index}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error seleccionando tarifa '{fare_type}' para tramo {leg_index}: {e}")
            try:
                self.take_screenshot(f"error_fare_{fare_type}_{leg_index}")
            except:
                pass
            return False