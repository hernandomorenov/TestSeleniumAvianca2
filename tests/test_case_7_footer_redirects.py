"""
Caso de prueba 7: Redirecciones del Footer en múltiples idiomas
Versión simplificada - Recorre Español, English, Français, Português
"""
import pytest
import allure
import time
from pages.home_page import HomePage
from utils.logger import logger


@allure.epic("FLYR Automation Suite")
@allure.feature("Navigation Tests - Multiidioma")
@allure.story("Redirecciones del Footer en 4 idiomas")
@pytest.mark.redirects
@pytest.mark.multilanguage
class TestCase7FooterRedirects:
    """Caso 7: Probar footer links en Español, English, Français, Português"""
    
    # Idiomas a probar (en orden)
    LANGUAGES = ["Español", "English", "Français", "Português"]
    
    # Links del footer (4 según CSV)
    FOOTER_LINKS = [
        "Somos avianca",
        "Sostenibilidad",
        "Plan de accesibilidad",
        "Información legal"
    ]
    
    @allure.title("Test 7: Footer redirects multiidioma - {browser}")
    @allure.description("Probar 4 links del footer en 4 idiomas diferentes")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("footer", "multilanguage", "redirects")
    def test_footer_redirects_multilanguage(self, driver, setup_test):
        """Test que recorre todos los idiomas automáticamente"""
        
        # Inicializar página
        home_page = HomePage(driver)
        all_results = {}
        
        # ==================== 1. EMPEZAR CON ESPAÑOL ====================
        with allure.step("1. Iniciar con idioma Español"):
            home_page.navigate_to(setup_test)
            time.sleep(3)
            
            # Verificar que estamos en español
            current_lang = home_page.get_current_language()
            logger.info(f"Idioma inicial: {current_lang}")
            
            # Si no está en español, cambiarlo
            if "Español" not in current_lang:
                home_page.select_language("Español")
                time.sleep(2)
        
        # ==================== 2. RECORRER TODOS LOS IDIOMAS ====================
        for language in self.LANGUAGES:
            language_results = []
            
            with allure.step(f"2. Probar en idioma: {language}"):
                # Cambiar idioma si no es el actual
                if language != "Español" or len(all_results) > 0:
                    home_page.select_language(language)
                    time.sleep(2)
                
                # Tomar screenshot del idioma
                home_page.take_screenshot(f"idioma_{language}")
                
                # ==================== 3. PROBAR LOS 4 LINKS ====================
                logger.info(f"=== Probando footer links en {language} ===")
                
                for i, link_name in enumerate(self.FOOTER_LINKS, 1):
                    with allure.step(f"  Link {i}: {link_name}"):
                        try:
                            # Scroll al footer
                            home_page.scroll_to_footer()
                            time.sleep(0.5)
                            
                            # URL antes del click
                            url_before = driver.current_url
                            
                            # Click en el link
                            click_ok = home_page.click_footer_link(link_name)
                            
                            if click_ok:
                                # Esperar redirección
                                time.sleep(2)
                                
                                # URL después del click
                                url_after = driver.current_url
                                
                                # Verificar si cambió
                                url_changed = url_before != url_after
                                
                                # Resultado
                                result = {
                                    "link": link_name,
                                    "click_ok": True,
                                    "url_changed": url_changed,
                                    "url_before": url_before[:60],
                                    "url_after": url_after[:60]
                                }
                                
                                # Tomar screenshot
                                home_page.take_screenshot(f"{language}_{link_name.replace(' ', '_')}")
                                
                                logger.info(f"  ✓ {link_name}: {'URL cambió' if url_changed else 'URL igual'}")
                                
                            else:
                                result = {
                                    "link": link_name,
                                    "click_ok": False,
                                    "error": "Click falló"
                                }
                                logger.warning(f"  ✗ {link_name}: No se pudo hacer click")
                        
                        except Exception as e:
                            result = {
                                "link": link_name,
                                "click_ok": False,
                                "error": str(e)
                            }
                            logger.error(f"  ✗ {link_name}: Error - {e}")
                        
                        language_results.append(result)
                        
                        # Volver atrás si no es el último link
                        if i < len(self.FOOTER_LINKS):
                            driver.back()
                            time.sleep(2)
                            
                            # Re-seleccionar idioma después de volver
                            home_page.select_language(language)
                            time.sleep(1)
                
                # Guardar resultados de este idioma
                all_results[language] = language_results
                
                # Ir a página principal para siguiente idioma (si no es el último)
                if language != self.LANGUAGES[-1]:
                    home_page.navigate_to(setup_test)
                    time.sleep(2)
        
        # ==================== 4. ANALIZAR RESULTADOS ====================
        with allure.step("4. Resultados finales"):
            self._generate_final_report(all_results)
            
            # Verificaciones finales
            total_success = 0
            for language, results in all_results.items():
                successful_clicks = sum(1 for r in results if r.get("click_ok", False))
                total_success += successful_clicks
                
                logger.info(f"{language}: {successful_clicks}/4 clicks exitosos")
            
            # Assert mínimo
            expected_min = len(self.LANGUAGES) * 3  # 3 de 4 en cada idioma
            assert total_success >= expected_min, (
                f"Clicks exitosos insuficientes: {total_success}/{expected_min}"
            )
            
            logger.info(f"✅ Test completado: {total_success}/{len(self.LANGUAGES)*4} clicks exitosos")
            return all_results
    
    def _generate_final_report(self, all_results):
        """Generar reporte simple de resultados"""
        report = "RESUMEN DEL TEST MULTIIDIOMA\n"
        report += "=" * 50 + "\n\n"
        
        for language, results in all_results.items():
            successful_clicks = sum(1 for r in results if r.get("click_ok", False))
            successful_redirects = sum(1 for r in results if r.get("url_changed", False))
            
            report += f"IDIOMA: {language}\n"
            report += f"  • Clicks exitosos: {successful_clicks}/4\n"
            report += f"  • Redirecciones exitosas: {successful_redirects}/4\n"
            
            for result in results:
                status = "✓" if result.get("click_ok") else "✗"
                redirect = "→" if result.get("url_changed") else "="
                report += f"    {status} {redirect} {result['link']}\n"
            
            report += "\n"
        
        # Totales
        total_clicks = sum(
            sum(1 for r in results if r.get("click_ok", False))
            for results in all_results.values()
        )
        total_redirects = sum(
            sum(1 for r in results if r.get("url_changed", False))
            for results in all_results.values()
        )
        
        report += f"TOTALES:\n"
        report += f"  • Clicks: {total_clicks}/{len(self.LANGUAGES)*4}\n"
        report += f"  • Redirecciones: {total_redirects}/{len(self.LANGUAGES)*4}\n"
        
        # Adjuntar a Allure
        allure.attach(report, name="Resumen Multiidioma", attachment_type=allure.attachment_type.TEXT)
        
        return report
    
    @allure.title("Test 7b: Quick footer test - {browser}")
    @allure.description("Test rápido - Solo 1 link por idioma")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("footer", "quick")
    def test_quick_footer_multilanguage(self, driver, setup_test):
        """Test rápido que prueba solo 1 link en cada idioma"""
        
        home_page = HomePage(driver)
        results = []
        
        with allure.step("1. Navegar a página"):
            home_page.navigate_to(setup_test)
            time.sleep(2)
        
        # Probar solo el primer link en cada idioma
        test_link = "Somos avianca"
        
        for language in self.LANGUAGES:
            with allure.step(f"2. Probar en {language}"):
                # Cambiar idioma
                if language != "Español" or len(results) > 0:
                    home_page.select_language(language)
                    time.sleep(2)
                
                # Scroll y click
                home_page.scroll_to_footer()
                time.sleep(0.5)
                
                url_before = driver.current_url
                click_ok = home_page.click_footer_link(test_link)
                
                if click_ok:
                    time.sleep(2)
                    url_after = driver.current_url
                    
                    results.append({
                        "language": language,
                        "link": test_link,
                        "success": True,
                        "url_changed": url_before != url_after
                    })
                    
                    logger.info(f"{language}: Click en {test_link} - {'URL cambió' if url_before != url_after else 'URL igual'}")
                    
                    # Volver atrás
                    driver.back()
                    time.sleep(2)
                else:
                    results.append({
                        "language": language,
                        "link": test_link,
                        "success": False
                    })
                    logger.warning(f"{language}: No se pudo clickear {test_link}")
        
        # Verificación
        successful_tests = sum(1 for r in results if r.get("success", False))
        assert successful_tests >= 3, f"Solo {successful_tests}/4 idiomas funcionaron"
        
        logger.info(f"✅ Test rápido completado: {successful_tests}/4 idiomas OK")
        return results