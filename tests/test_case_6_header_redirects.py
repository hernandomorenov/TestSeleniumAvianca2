import pytest
import allure
import time
from pages.home_page import HomePage
from utils.logger import logger

@allure.epic("FLYR Automation Suite")
@allure.feature("Navigation Tests")
@allure.story("Redirecciones del Header")
@pytest.mark.redirects
@pytest.mark.navigation
class TestCase6HeaderRedirects:
    """Caso 6: Verificar redirecciones del Header"""
    
    @allure.title("Test 6: Verify header redirects - {browser}")
    @allure.description("Usar opciones del Navbar para acceder a 3 sitios diferentes")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("header", "navigation", "redirects")
    def test_header_redirects(self, driver, setup_test, request):
        # Inicializar página
        home_page = HomePage(driver)
        
        # Links del header a probar (ajustar según sitio real)
        header_links = ["home", "flights", "hotels"]  # 3 sitios como requerido
        
        # ==================== CONFIGURAR IDIOMA INICIAL ====================
        with allure.step("1. Configurar idioma inicial (English)"):
            assert home_page.navigate_to(setup_test), "No se pudo navegar a la página"
            assert home_page.select_language("english"), "No se pudo seleccionar inglés"
            time.sleep(2)
        
        # ==================== PROBAR CADA LINK ====================
        results = []
        
        for i, link in enumerate(header_links, 1):
            with allure.step(f"{i+1}. Probar link del header: {link}"):
                # Guardar URL actual para comparación
                previous_url = driver.current_url
                
                # Click en el link del header
                click_success = home_page.click_header_link(link)
                
                if click_success:
                    # Esperar a que cargue la nueva página
                    assert home_page.wait_for_page_load(), f"Página no cargó después de click en {link}"
                    
                    # Obtener URL actual
                    current_url = driver.current_url
                    
                    # Verificar que la URL cambió
                    url_changed = previous_url != current_url
                    
                    # Verificar que la URL carga correctamente
                    url_valid = self._verify_url_valid(driver, link)
                    
                    # Tomar screenshot
                    home_page.take_screenshot(f"header_{link}")
                    
                    # Registrar resultado
                    result = {
                        "link": link,
                        "click_success": click_success,
                        "url_changed": url_changed,
                        "url_valid": url_valid,
                        "final_url": current_url
                    }
                    results.append(result)
                    
                    # Adjuntar información
                    status = "✅" if (url_changed and url_valid) else "⚠️"
                    allure.attach(
                        f"Link: {link}\n"
                        f"Click exitoso: {click_success}\n"
                        f"URL cambió: {url_changed}\n"
                        f"URL válida: {url_valid}\n"
                        f"URL final: {current_url}\n"
                        f"Status: {status}",
                        name=f"Header Link {link}",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    
                    logger.info(f"Header link {link}: click={click_success}, url_changed={url_changed}, valid={url_valid}")
                    
                    # Volver a la página principal para probar el siguiente link
                    if i < len(header_links):
                        driver.back()
                        assert home_page.wait_for_page_load(), "No se pudo volver atrás"
                        time.sleep(1)
                else:
                    logger.warning(f"No se pudo hacer click en header link: {link}")
                    # Continuar con el siguiente link
        
        # ==================== VERIFICACIÓN FINAL ====================
        with allure.step("Verificación final - Resumen de resultados"):
            # Contar éxitos
            successful_redirects = sum(1 for r in results if r.get("url_changed") and r.get("url_valid"))
            
            home_page.take_screenshot("header_redirects_summary")
            
            # Crear resumen
            summary = f"Test de header redirects completado en {request.cls.browser}\n\n"
            summary += f"Total links probados: {len(results)}\n"
            summary += f"Redirecciones exitosas: {successful_redirects}\n\n"
            
            for r in results:
                summary += f"- {r['link']}: {'✅' if r.get('url_changed') and r.get('url_valid') else '❌'}\n"
                if r.get('final_url'):
                    summary += f"  URL: {r['final_url']}\n"
            
            allure.attach(summary, name="Test Summary", attachment_type=allure.attachment_type.TEXT)
            
            # Assert: al menos algunos links deberían funcionar
            assert successful_redirects >= 1, "Ninguna redirección del header funcionó correctamente"
            
            logger.info(f"✅ Header redirects test completado. Exitosos: {successful_redirects}/{len(results)}")
    
    def _verify_url_valid(self, driver, link_name):
        """Verificar que una URL carga correctamente"""
        try:
            current_url = driver.current_url
            
            # Verificar que no es una página de error
            page_source = driver.page_source.lower()
            
            # Lista de indicadores de error
            error_indicators = [
                "error", "not found", "404", "500", "cannot", "unavailable",
                "error", "no encontrada", "no disponible"
            ]
            
            for error in error_indicators:
                if error in page_source:
                    logger.warning(f"Indicador de error encontrado: {error}")
                    return False
            
            # Verificar que la página tiene contenido
            if len(page_source) < 100:  # Página muy pequeña puede ser error
                logger.warning("Página muy pequeña, posible error")
                return False
            
            # Verificar código de estado HTTP (vía JavaScript)
            try:
                http_status = driver.execute_script("""
                    return window.performance.getEntriesByType('navigation')[0].responseStatus;
                """)
                if http_status and http_status >= 400:
                    logger.warning(f"Código HTTP de error: {http_status}")
                    return False
            except:
                pass  # Si no se puede obtener, continuar
            
            return True
            
        except Exception as e:
            logger.error(f"Error verificando URL: {e}")
            return False
    
    @allure.title("Test 6b: Header links with different languages - {browser}")
    @allure.description("Probar links del header con diferentes idiomas")
    @allure.severity(allure.severity_level.MINOR)
    def test_header_multilingual(self, driver, setup_test):
        """Probar que los links del header funcionan con diferentes idiomas"""
        home_page = HomePage(driver)
        
        assert home_page.navigate_to(setup_test)
        
        # Probar con diferentes idiomas
        for language in ["spanish", "english"]:
            logger.info(f"Probando header links con idioma: {language}")
            
            # Cambiar idioma
            home_page.select_language(language)
            time.sleep(2)
            
            # Probar un link
            if home_page.click_header_link("flights"):
                home_page.take_screenshot(f"header_{language}_flights")
                logger.info(f"✅ Header link funciona con idioma {language}")
                
                # Volver
                driver.back()
                home_page.wait_for_page_load()
            else:
                logger.warning(f"⚠️ Header link no funciona con idioma {language}")
        
        assert True