import pytest
import os
import sys
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Importar utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.config import Config
from utils.video_recorder import VideoRecorder
from utils.screenshot_manager import ScreenshotManager

# ==================== FIXTURES PARA MULTI-NAVEGADOR ====================

def get_chrome_options(headless=False):
    """Opciones optimizadas para Chrome"""
    options = ChromeOptions()
    
    # Configuraciones para velocidad
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    
    # Optimizaciones de rendimiento
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Preferencias
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.images": 1,
    }
    options.add_experimental_option("prefs", prefs)
    
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    return options

def get_firefox_options(headless=False):
    """Opciones optimizadas para Firefox"""
    options = FirefoxOptions()
    
    if headless:
        options.add_argument("--headless")
    
    # Configuraciones de rendimiento
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference('useAutomationExtension', False)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    
    return options

def get_edge_options(headless=False):
    """Opciones optimizadas para Edge"""
    options = EdgeOptions()
    
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    return options

def setup_driver(browser_name, headless):
    """Configurar driver según el navegador"""
    logger.info(f"Configurando driver para {browser_name.upper()} (headless={headless})")
    
    try:
        if browser_name.lower() == "chrome":
            options = get_chrome_options(headless)
            
            # Usar webdriver-manager para manejo automático
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                logger.warning(f"WebDriver Manager falló: {e}. Usando driver local.")
                driver = webdriver.Chrome(options=options)
        
        elif browser_name.lower() == "firefox":
            options = get_firefox_options(headless)
            
            try:
                from webdriver_manager.firefox import GeckoDriverManager
                service = FirefoxService(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=options)
            except Exception as e:
                logger.warning(f"WebDriver Manager falló: {e}. Usando driver local.")
                driver = webdriver.Firefox(options=options)
        
        elif browser_name.lower() == "edge":
            options = get_edge_options(headless)
            
            try:
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                service = EdgeService(EdgeChromiumDriverManager().install())
                driver = webdriver.Edge(service=service, options=options)
            except Exception as e:
                logger.warning(f"WebDriver Manager falló: {e}. Usando driver local.")
                driver = webdriver.Edge(options=options)
        
        else:
            raise ValueError(f"Navegador no soportado: {browser_name}")
        
        # Configurar timeouts optimizados
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(20)
        driver.implicitly_wait(5)  # Timeout corto para mayor velocidad
        
        logger.info(f"Driver {browser_name.upper()} configurado exitosamente")
        return driver
        
    except Exception as e:
        logger.error(f"Error configurando driver {browser_name}: {e}")
        raise

@pytest.fixture(scope="function", params=["chrome", "firefox", "edge"])
def driver(request):
    """Fixture principal para multi-navegador"""
    browser_name = request.param
    headless = request.config.getoption("--headless")
    
    # Iniciar grabación de video
    video_recorder = VideoRecorder()
    test_name = f"{request.node.name}_{browser_name}"
    video_recorder.start_recording(test_name)
    
    # Configurar driver
    driver = setup_driver(browser_name, headless)
    
    # Configurar screenshot manager
    screenshot_manager = ScreenshotManager(driver)
    
    # Pasar contexto al test
    request.cls.driver = driver
    request.cls.browser = browser_name
    request.cls.video_recorder = video_recorder
    request.cls.screenshot_manager = screenshot_manager
    
    yield driver
    
    # Finalizar grabación y adjuntar a Allure
    video_path = video_recorder.stop_recording()
    if video_path and os.path.exists(video_path):
        import allure
        with open(video_path, 'rb') as video_file:
            allure.attach(video_file.read(), 
                         name=f"video_{test_name}", 
                         attachment_type=allure.attachment_type.MP4)
    
    # Cerrar driver
    driver.quit()
    logger.info(f"Driver {browser_name.upper()} cerrado")

@pytest.fixture(scope="function")
def setup_test(request):
    """Setup para cada test"""
    # Crear directorios si no existen
    directories = ["reports", "screenshots", "videos", "logs"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Configurar URL base
    url = request.config.getoption("--url")
    logger.info(f"URL base configurada: {url}")
    print(f"URL: {url}")
    
    yield url

# ==================== HOOKS Y CONFIGURACIONES ====================

def pytest_addoption(parser):
    """Agregar opciones de línea de comandos"""
    parser.addoption("--browser", action="store", default="chrome",
                     help="Navegador para pruebas: chrome, firefox, edge")
    parser.addoption("--headless", action="store_true", default=False,
                     help="Ejecutar en modo headless")
    parser.addoption("--url", action="store", default=Config.BASE_URL_4,
                     help=f"URL base (default: {Config.BASE_URL_4})")
    parser.addoption("--slow", action="store_true", default=False,
                     help="Ejecutar con timeouts más largos")
    parser.addoption("--record-video", action="store_true", default=True,
                     help="Grabar video de las ejecuciones")
    parser.addoption("--clean-reports", action="store_true", default=False,
                     help="Limpiar reportes anteriores")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Tomar screenshot automático en fallos"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Verificar si hay driver disponible
        if hasattr(item.cls, 'driver') and item.cls.driver:
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_name = f"{item.name}_{timestamp}.png"
                screenshot_path = os.path.join("screenshots", screenshot_name)
                
                item.cls.driver.save_screenshot(screenshot_path)
                logger.info(f"Screenshot de fallo guardado: {screenshot_path}")
                
                # Adjuntar a reporte Allure
                import allure
                with open(screenshot_path, 'rb') as f:
                    allure.attach(f.read(), name="screenshot_on_failure",
                                 attachment_type=allure.attachment_type.PNG)
                    
            except Exception as e:
                logger.error(f"Error tomando screenshot: {e}")

def pytest_sessionstart(session):
    """Inicio de sesión de pruebas"""
    logger.info("=" * 60)
    logger.info("INICIANDO SESIÓN DE PRUEBAS AUTOMATIZADAS")
    logger.info("=" * 60)
    
    # Limpiar reportes antiguos si se solicita
    if session.config.getoption("--clean-reports"):
        import shutil
        for folder in ["reports/allure-results", "screenshots", "videos"]:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                logger.info(f"Carpeta limpiada: {folder}")

def pytest_sessionfinish(session, exitstatus):
    """Fin de sesión de pruebas"""
    logger.info("=" * 60)
    logger.info("SESIÓN DE PRUEBAS FINALIZADA")
    logger.info(f"Exit status: {exitstatus}")
    logger.info("=" * 60)
    
    # Generar reporte Allure si hay resultados
    allure_dir = "reports/allure-results"
    if os.path.exists(allure_dir) and os.listdir(allure_dir):
        logger.info("Generando reporte Allure...")
        try:
            import subprocess
            subprocess.run([
                "allure", "generate", allure_dir,
                "--clean", "-o", "reports/allure-report"
            ], check=True)
            logger.info("✅ Reporte Allure generado: reports/allure-report/index.html")
        except Exception as e:
            logger.error(f"❌ Error generando reporte Allure: {e}")