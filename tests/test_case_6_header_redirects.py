import pytest
import allure
import time
from selenium.webdriver.common.by import By  # ¡IMPORTANTE! Falta este import
from pages.home_page import HomePage
from utils.logger import logger

LANGUAGES = ["Español", "English", "Português", "Français"]

@allure.epic("FLYR Automation Suite")
@allure.feature("Navigation Tests")
class TestCase6HeaderRedirects:

    @allure.title("Test Header Navigation por idioma")
    @pytest.mark.parametrize("language", LANGUAGES)
    def test_csv_header_navigation(self, driver, setup_test, language):
        home = HomePage(driver)
        home.navigate_to(setup_test)

        # Seleccionar idioma
        with allure.step(f"Seleccionar idioma: {language}"):
            try:
                success = home.select_language(language)
                if not success:
                    logger.warning(f"No se pudo cambiar a {language}, continuando con español")
            except Exception as e:
                logger.error(f"Error con método select_language: {e}")

        steps = [
            {"action": "click", "key": "Reservar", "desc": "Click en Reservar/Book"},
            {"action": "scroll", "direction": "down", "desc": "Scroll Down"},
            {"action": "scroll", "direction": "up", "desc": "Scroll Up"},
            {"action": "click", "key": "Ofertas y destinos", "desc": "Click en Ofertas y destinos"},
            {"action": "click", "key": "Destinos", "desc": "Click en Destinos"},
            {"action": "scroll", "direction": "down", "desc": "Scroll Down"},
            {"action": "click", "key": "Información y ayuda", "desc": "Click en Información y ayuda"},
            {"action": "click", "key": "Tipos de tarifas", "desc": "Click en Tipos de tarifas"},
        ]
        
        failures = []
        
        for i, step in enumerate(steps, 1):
            with allure.step(f"Paso {i}: {step['desc']}"):
                try:
                    if step["action"] == "click":
                        # Intentar diferentes textos según el idioma
                        if language == "English":
                            text_map = {
                                "Reservar": "Book",
                                "Ofertas y destinos": "Offers and destinations",
                                "Destinos": "Our destinations",
                                "Información y ayuda": "Information and help",
                                "Tipos de tarifas": "Types of fares"
                            }
                        elif language == "Português":
                            text_map = {
                                "Reservar": "Reservar",
                                "Ofertas y destinos": "Ofertas e destinos",
                                "Destinos": "Nossos destinos",
                                "Información y ayuda": "Informação e assistência",
                                "Tipos de tarifas": "Tipos de taxas"
                            }
                        elif language == "Français":
                            text_map = {
                                "Reservar": "Réserver",
                                "Ofertas y destinos": "Offres et destinations",
                                "Destinos": "Destinations",
                                "Información y ayuda": "Information et aide",
                                "Tipos de tarifas": "Types de tarifs"
                            }
                        else:  # Español
                            text_map = {
                                "Reservar": "Reservar",
                                "Ofertas y destinos": "Ofertas y destinos",
                                "Destinos": "Destinos",
                                "Información y ayuda": "Información y ayuda",
                                "Tipos de tarifas": "Tipos de tarifas"
                            }
                        
                        text = text_map.get(step["key"], step["key"])
                        
                        # Método simple de click por texto
                        xpath = f"//*[contains(text(), '{text}')]"
                        elements = driver.find_elements(By.XPATH, xpath)
                        
                        clicked = False
                        for element in elements:
                            try:
                                if element.is_displayed() and element.is_enabled():
                                    # Resaltar el elemento
                                    driver.execute_script("arguments[0].style.border='3px solid red';", element)
                                    time.sleep(0.3)
                                    
                                    # Scroll al elemento
                                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                                    time.sleep(0.5)
                                    
                                    # Intentar click
                                    try:
                                        element.click()
                                    except:
                                        driver.execute_script("arguments[0].click();", element)
                                    
                                    # Quitar resaltado
                                    driver.execute_script("arguments[0].style.border='none';", element)
                                    
                                    clicked = True
                                    logger.info(f"✓ Click en '{text}' ({step['key']})")
                                    break
                            except Exception as e:
                                logger.debug(f"Error con elemento: {e}")
                                continue
                        
                        if not clicked:
                            failures.append(f"No se pudo hacer click en: {step['key']}")
                            logger.warning(f"❌ No se pudo hacer click en: {step['key']}")
                    
                    elif step["action"] == "scroll":
                        pixels = 500 if step["direction"] == "down" else -500
                        driver.execute_script(f"window.scrollBy(0, {pixels});")
                        logger.info(f"✓ Scroll {step['direction']}")
                    
                    # Tomar screenshot después de cada paso
                    try:
                        home.take_screenshot(f"paso_{i}_{step['key'].replace(' ', '_')}")
                    except:
                        pass
                    
                    time.sleep(1)
                    
                except Exception as e:
                    failures.append(f"Error en paso {step['desc']}: {str(e)}")
                    logger.error(f"Error en paso {step['desc']}: {e}")
        
        # Reporte final
        if failures:
            failure_msg = f"Fallos en idioma '{language}':\n" + "\n".join(failures)
            allure.attach(failure_msg, name=f"Fallos {language}", attachment_type=allure.attachment_type.TEXT)
            
            # Si hay demasiados fallos, marcar como fallido
            if len(failures) > 3:
                pytest.fail(f"Demasiados fallos en idioma '{language}': {len(failures)}")
            else:
                logger.warning(f"Algunos fallos en '{language}' pero continuando: {failures}")
    
   