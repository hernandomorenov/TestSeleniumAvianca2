"""
Debug script para inspeccionar la estructura HTML de la página de resultados de vuelos
y encontrar los selectores correctos para el botón de precio
"""
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config import Config
from utils.logger import logger

# Configurar driver
config = Config()
driver = webdriver.Chrome()

try:
    # Navegar a home
    logger.info("🌐 Navegando a home...")
    driver.get(config.BASE_URL)
    time.sleep(3)
    
    # Seleccionar idioma
    logger.info("🔧 Seleccionando English...")
    lang_dropdown = driver.find_element(By.XPATH, "//button[@role='button'][contains(@class, 'language')]")
    lang_dropdown.click()
    time.sleep(1)
    english = driver.find_element(By.XPATH, "//div[contains(text(), 'English')]")
    english.click()
    time.sleep(2)
    
    # Aplicar COP
    logger.info("🔧 Aplicando COP...")
    pos_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'pos')]")
    pos_btn.click()
    time.sleep(1)
    cop_radio = driver.find_element(By.XPATH, "//label[contains(text(), 'COP')]")
    cop_radio.click()
    time.sleep(1)
    apply_btn = driver.find_element(By.XPATH, "//span[contains(text(), 'Apply')]")
    apply_btn.click()
    time.sleep(2)
    
    # Seleccionar One-way
    logger.info("🔧 Seleccionando One-way...")
    oneway = driver.find_element(By.ID, "oneway")
    oneway.click()
    time.sleep(1)
    
    # Destino MDE
    logger.info("🔧 Seleccionando destino MDE...")
    dest_input = driver.find_element(By.ID, "destino")
    dest_input.click()
    time.sleep(1)
    mde_option = driver.find_element(By.XPATH, "//span[contains(text(), 'MDE')]")
    mde_option.click()
    time.sleep(1)
    
    # Fecha
    logger.info("🔧 Seleccionando fecha...")
    date_input = driver.find_element(By.ID, "fecha_ida")
    date_input.click()
    time.sleep(1)
    day_16 = driver.find_element(By.XPATH, "//span[text()='16']")
    day_16.click()
    time.sleep(1)
    
    # Pasajeros
    logger.info("🔧 Confirmando 1 pasajero...")
    confirm_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm')]")
    confirm_btn.click()
    time.sleep(1)
    
    # CLICK SEARCH
    logger.info("🔍 Haciendo click en SEARCH...")
    search_btn = driver.find_element(By.ID, "searchButton")
    search_btn.click()
    
    # ESPERAR RESULTADOS
    logger.info("⏳ Esperando resultados de vuelos (20 segundos)...")
    time.sleep(20)
    
    # CAPTURAR PÁGINA
    logger.info("📸 Capturando página de resultados...")
    driver.save_screenshot("flight_results_page.png")
    
    # ANALIZAR HTML
    logger.info("\n" + "="*80)
    logger.info("ANALIZANDO ESTRUCTURA HTML DE RESULTADOS")
    logger.info("="*80)
    
    # Buscar todos los posibles selectores
    selectors_to_test = [
        ("//button[contains(text(),'From COP')]", "From COP button"),
        ("//button[contains(@class,'journey_price_button')]", "journey_price_button"),
        ("//div[@class='journey_price_section']//button", "journey_price_section button"),
        ("(//button[contains(text(),'From')])[1]", "First From button"),
        ("//button[contains(text(),'COP')]", "COP button"),
        ("//div[contains(@class,'journey_price')]", "journey_price div"),
        ("//div[contains(@class,'fare')]", "fare div"),
        ("//button[@aria-label]", "buttons with aria-label"),
        ("//div[@role='button']", "divs with role=button"),
        ("//span[@class='button_label']", "button_label spans"),
    ]
    
    for selector, description in selectors_to_test:
        try:
            elements = driver.find_elements(By.XPATH, selector)
            if elements:
                logger.info(f"\n✓ {description} ({selector})")
                logger.info(f"  Found {len(elements)} element(s)")
                for i, elem in enumerate(elements[:3]):  # Mostrar primeros 3
                    try:
                        text = elem.text.strip()[:100]
                        classes = elem.get_attribute("class")
                        logger.info(f"    [{i+1}] Text: {text}")
                        if classes:
                            logger.info(f"        Class: {classes}")
                    except:
                        pass
            else:
                logger.info(f"\n✗ {description} - No elements found")
        except Exception as e:
            logger.info(f"\n✗ {description} - Error: {e}")
    
    # BUSCAR TODOS LOS BOTONES
    logger.info(f"\n" + "="*80)
    logger.info("TODOS LOS BOTONES EN LA PÁGINA:")
    logger.info("="*80)
    buttons = driver.find_elements(By.TAG_NAME, "button")
    logger.info(f"\nTotal botones: {len(buttons)}")
    for i, btn in enumerate(buttons[:10]):
        try:
            text = btn.text.strip()[:80]
            classes = btn.get_attribute("class")
            logger.info(f"[{i+1}] {text}")
            if classes:
                logger.info(f"     {classes}")
        except:
            pass
    
    # BUSCAR DIVS CON CONTENIDO DE PRECIO
    logger.info(f"\n" + "="*80)
    logger.info("DIVS CON CONTENIDO DE PRECIO:")
    logger.info("="*80)
    price_divs = driver.find_elements(By.XPATH, "//*[contains(text(),'COP') or contains(text(),'$')]")
    logger.info(f"\nElements with price content: {len(price_divs)}")
    for i, div in enumerate(price_divs[:5]):
        try:
            text = div.text.strip()[:100]
            logger.info(f"[{i+1}] {text}")
        except:
            pass
    
    logger.info("\n✅ Análisis completado. Ver flight_results_page.png")
    
finally:
    driver.quit()
    logger.info("🔌 Driver cerrado")
