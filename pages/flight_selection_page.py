from selenium.webdriver.common.by import By
import allure
from pages.base_page import BasePage
from utils.logger import logger

class FlightSelectionPage(BasePage):
    """Página de selección de vuelos"""
    
    # ==================== SELECTORES  ====================
    
    # Fare selection 
    SELECT_FARE_ELEMENT = (By.XPATH, "//div[contains(text(), 'Select fare')]")
    
    # Basic fare 
    BASIC_FARE_SELECT = (By.XPATH, "//div[@aria-label='Click to select Basic fare']//div[contains(@class, 'fare_button_label')]")
    
    # Continue button
    CONTINUE_BUTTON_CSV = (By.XPATH, "//button[contains(@class, 'btn-action')]//span[contains(text(), 'Continue')]")
    
    # ==================== SELECTORES ORIGINALES ====================
    
    # Fare types
    BASIC_FARE = (By.XPATH, "//div[contains(@class, 'basic-fare')]//button[contains(text(), 'Select')]")
    PLUS_FARE = (By.XPATH, "//div[contains(@class, 'plus-fare')]//button[contains(text(), 'Select')]")
    PREMIUM_FARE = (By.XPATH, "//div[contains(@class, 'premium-fare')]//button[contains(text(), 'Select')]")
    
    # Departure flight
    DEPARTURE_FLIGHTS = (By.XPATH, "//div[contains(@class, 'departure-flights')]//button[contains(text(), 'Select')]")
    DEPARTURE_FLIGHT_PRICE = (By.XPATH, "//div[contains(@class, 'flight-price')]")
    
    # Continue button original
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(text(), 'Continue') or contains(@class, 'continue-button')]")
    
    # ==================== MÉTODOS SEGÚN CSV ====================
    
    @allure.step("Select fare according to CSV steps")
    def select_fare_csv(self):
        """Seleccionar tarifa según pasos CSV"""
        logger.info("Seleccionando tarifa según CSV")
        
        try:
            # Scroll down (CSV paso 19)
            self.scroll_down(500)
            self.wait(2)
            
            # Click en "Select fare" (CSV paso 20)
            self.click(self.SELECT_FARE_ELEMENT, "Select fare element")
            self.wait(1)
            
            # Scroll up (CSV paso 21)
            self.scroll_up(200)
            self.wait(1)
            
            # Scroll down y up adicionales (CSV pasos 22-23)
            self.scroll_down(400)
            self.wait(0.5)
            self.scroll_up(200)
            self.wait(0.5)
            
            # Seleccionar tarifa Basic (CSV paso 24)
            self.click(self.BASIC_FARE_SELECT, "Basic fare select")
            self.wait(2)
            
            # Scroll down (CSV paso 25)
            self.scroll_down(600)
            self.wait(1)
            
            return True
        except Exception as e:
            logger.error(f"Error seleccionando tarifa según CSV: {e}")
            # Fallback a método original
            return self.select_fare_type("basic")
    
    @allure.step("Continue to next page CSV")
    def continue_csv(self):
        """Continuar según CSV"""
        logger.info("Continuando según CSV")
        
        try:
            # Click en Continue (CSV paso 26)
            self.click(self.CONTINUE_BUTTON_CSV, "Continue button CSV")
            self.wait(5)
            
            # Scroll down (CSV paso 27)
            self.scroll_down(300)
            self.wait(1)
            
            return True
        except Exception as e:
            logger.error(f"Error continuando según CSV: {e}")
            return self.continue_to_passengers()