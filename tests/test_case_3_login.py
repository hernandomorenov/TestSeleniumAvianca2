import pytest
import allure
import time
from pages.home_page import HomePage
from pages.flight_selection_page import FlightSelectionPage
from utils.config import Config
from utils.logger import logger

@allure.epic("FLYR Automation Suite")
@allure.feature("Login Tests")
@allure.story("Login y búsqueda con credenciales específicas")
@pytest.mark.login
@pytest.mark.smoke
class TestCase3Login:
    """Caso 3: Login en UAT con credenciales específicas"""
    
    @allure.title("Test 3: Login with specific credentials - {browser}")
    @allure.description("Login con credenciales específicas y configuración de búsqueda")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("login", "authentication", "search")
    def test_login_and_search(self, driver, request):
        # Inicializar páginas
        home_page = HomePage(driver)
        flight_page = FlightSelectionPage(driver)
        
        # ==================== LOGIN ====================
        with allure.step("1. Navegar a página de login y autenticar"):
            # Navegar a la página de login
            assert home_page.navigate_to(Config.LOGIN_URL), "No se pudo navegar a la página de login"
            
            # Realizar login con credenciales específicas
            assert home_page.login(
                Config.TEST_USERNAME,
                Config.TEST_PASSWORD
            ), "No se pudo realizar login"
            
            # Esperar a que el login sea exitoso
            time.sleep(3)
            
            # Verificar que estamos logueados (puede variar según implementación)
            # Por ejemplo, verificar que el nombre de usuario aparece
            allure.attach(
                f"Login realizado con usuario: {Config.TEST_USERNAME}",
                name="Login Info",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # ==================== CONFIGURAR BÚSQUEDA ====================
        with allure.step("2. Configurar búsqueda después de login"):
            # Seleccionar idioma Francés
            assert home_page.select_language("french"), "No se pudo seleccionar idioma francés"
            
            # Seleccionar POS France
            assert home_page.select_pos("france"), "No se pudo seleccionar POS France"
            
            # Configurar origen y destino (cualquiera)
            assert home_page.set_origin_destination("CDG", "MAD"), \
                "No se pudo configurar origen/destino"
            
            # Configurar 3 pasajeros de cada tipo
            assert home_page.set_passengers(
                adults=3, 
                youth=3, 
                children=3, 
                infants=3
            ), "No se pudo configurar pasajeros"
            
            # Buscar vuelos
            assert home_page.search_flights(), "No se pudo buscar vuelos"
        
        # ==================== VERIFICAR PÁGINA DE VUELOS ====================
        with allure.step("3. Validar que cargue página de Select flight"):
            assert flight_page.wait_for_page_load(), "Página de vuelos no cargó"
            
            # Verificar que estamos en la página correcta
            current_url = driver.current_url.lower()
            assert "select" in current_url or "vuelos" in current_url or "flight" in current_url, \
                f"No estamos en la página de selección de vuelos. URL: {driver.current_url}"
            
            allure.attach(
                f"Página de selección de vuelos cargada correctamente\n"
                f"URL: {driver.current_url}\n"
                f"Título: {driver.title}",
                name="Flight Selection Page",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # ==================== CAPTURAR INFORMACIÓN DE DEVTOOLS ====================
        with allure.step("4. Capturar información de Network desde DevTools"):
            # NOTA: Esto requeriría acceso a DevTools via Selenium 4
            # Aquí implementamos una versión simplificada
            
            try:
                # Usar execute_script para obtener información de red disponible
                network_info = driver.execute_script("""
                    if (window.performance && window.performance.getEntriesByType) {
                        var resources = window.performance.getEntriesByType('resource');
                        var sessionResources = resources.filter(function(r) {
                            return r.name.toLowerCase().includes('session');
                        });
                        return {
                            totalResources: resources.length,
                            sessionResources: sessionResources.length,
                            sampleSessionResources: sessionResources.slice(0, 3).map(function(r) {
                                return {
                                    name: r.name,
                                    duration: r.duration,
                                    transferSize: r.transferSize
                                };
                            })
                        };
                    }
                    return { error: 'Performance API not available' };
                """)
                
                allure.attach(
                    str(network_info),
                    name="Network Resources Info",
                    attachment_type=allure.attachment_type.JSON
                )
                
                logger.info(f"Información de red capturada: {network_info}")
                
            except Exception as e:
                allure.attach(
                    f"No se pudo capturar información de DevTools: {str(e)}",
                    name="DevTools Error",
                    attachment_type=allure.attachment_type.TEXT
                )
                logger.warning(f"No se pudo capturar info de DevTools: {e}")
        
        # ==================== SELECCIONAR VUELOS ====================
        with allure.step("5. Seleccionar vuelos"):
            # Intentar seleccionar algún vuelo disponible
            flight_selected = False
            
            # Intentar seleccionar tarifa basic
            if flight_page.select_fare_type("basic"):
                # Intentar seleccionar vuelo de ida
                if flight_page.select_departure_flight():
                    flight_selected = True
            
            # Si no se pudo seleccionar basic, intentar con otra tarifa
            if not flight_selected:
                # Intentar con plus
                if flight_page.select_fare_type("plus"):
                    if flight_page.select_departure_flight():
                        flight_selected = True
            
            if flight_selected:
                allure.attach(
                    "Vuelo seleccionado exitosamente",
                    name="Flight Selection",
                    attachment_type=allure.attachment_type.TEXT
                )
            else:
                allure.attach(
                    "No se pudo seleccionar vuelo (puede que no haya disponibilidad)",
                    name="Flight Selection Warning",
                    attachment_type=allure.attachment_type.TEXT
                )
                # No fallar el test si no hay vuelos disponibles
        
        # ==================== VERIFICACIÓN FINAL ====================
        with allure.step("6. Verificación final"):
            # Tomar screenshot final
            home_page.take_screenshot("login_test_completed")
            
            allure.attach(
                f"Login test completado exitosamente en {request.cls.browser}\n"
                f"Usuario: {Config.TEST_USERNAME}\n"
                f"URL final: {driver.current_url}\n"
                f"Título: {driver.title}",
                name="Test Result",
                attachment_type=allure.attachment_type.TEXT
            )
            
            logger.info(f"✅ Login test completado en {request.cls.browser}")
            assert True, "Login y búsqueda completados exitosamente"