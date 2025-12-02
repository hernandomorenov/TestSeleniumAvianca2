import os

class Config:
    # URLs
    BASE_URL_4 = "https://nuxqa4.avtest.ink/"
    BASE_URL_5 = "https://nuxqa5.avtest.ink/"
    LOGIN_URL = "https://nuxqa3.avtest.ink/"
    
    # Credenciales
    TEST_USERNAME = "21734198706"
    TEST_PASSWORD = "Lifemiles1"
    
    # Timeouts (optimizados para velocidad)
    IMPLICIT_WAIT = 5
    EXPLICIT_WAIT = 15
    PAGE_LOAD_TIMEOUT = 30
    
    # Directorios
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
    REPORT_DIR = os.path.join(BASE_DIR, "reports")
    VIDEO_DIR = os.path.join(BASE_DIR, "videos")
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    DRIVER_DIR = os.path.join(BASE_DIR, "drivers")
    
    # Datos de prueba
    DEFAULT_ORIGIN = "BOG"  # Bogotá
    DEFAULT_DESTINATION = "MDE"  # Medellín
    
    # Configuración de navegadores
    BROWSERS = ["chrome", "firefox", "edge"]
    DEFAULT_BROWSER = "chrome"
    HEADLESS = True  # Para ejecución rápida
    
    # Idiomas
    LANGUAGES = {
        "spanish": "Español",
        "english": "English",
        "french": "Français",
        "portuguese": "Português"
    }
    
    # Países (POS)
    COUNTRIES = {
        "spain": "Spain",
        "chile": "Chile",
        "france": "France",
        "colombia": "Colombia",
        "mexico": "Mexico",
        "peru": "Peru"
    }
    
    # Tipos de tarifa
    FARE_TYPES = ["basic", "plus", "flex", "premium"]
    
    # Tipos de asientos
    SEAT_TYPES = ["economy", "plus", "premium", "business"]