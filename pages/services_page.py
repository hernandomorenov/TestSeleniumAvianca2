"""
Page Object para selección de servicios adicionales
"""
from selenium.webdriver.common.by import By
import allure
import time
from pages.base_page import BasePage
from utils.logger import logger

class ServicesPage(BasePage):
    """Página de servicios adicionales"""
    
    # ==================== LOCATORS ====================
    
    # Lounges
    LOUNGE_CHECKBOX = (By.ID, "lounge-service")
    LOUNGE_OPTION = (By.XPATH, "//label[contains(text(), 'Avianca Lounge')]")
    
    # Equipaje adicional
    EXTRA_BAGGAGE_CHECKBOX = (By.ID, "extra-baggage")
    BAGGAGE_OPTION_20KG = (By.XPATH, "//label[contains(text(), '20 kg')]")
    BAGGAGE_OPTION_30KG = (By.XPATH, "//label[contains(text(), '30 kg')]")
    
    # Asiento preferencial
    PREFERENTIAL_SEAT_CHECKBOX = (By.ID, "preferential-seat")
    
    # Seguro de viaje
    TRAVEL_INSURANCE_CHECKBOX = (By.ID, "travel-insurance")
    
    # Priority boarding
    PRIORITY_BOARDING_CHECKBOX = (By.ID, "priority-boarding")
    
    # Saltar servicios
    SKIP_SERVICES_BUTTON = (By.XPATH, "//button[contains(text(), 'Skip') or contains(text(), 'Saltar')]")
    
    # Continuar
    CONTINUE_BUTTON = (By.ID, "continue-services")
    
    # ==================== MÉTODOS ====================
    
    @allure.step("Seleccionar Avianca Lounge")
    def select_avianca_lounge(self):
        """Seleccionar servicio de Avianca Lounge"""
        logger.info("Seleccionando Avianca Lounge")
        
        success = self.click(self.LOUNGE_CHECKBOX, "Checkbox Lounge")
        
        if success:
            time.sleep(0.5)
            success = self.click(self.LOUNGE_OPTION, "Opción Avianca Lounge")
        
        return success
    
    @allure.step("Seleccionar equipaje adicional: {weight} kg")
    def select_extra_baggage(self, weight=20):
        """Seleccionar equipaje adicional"""
        logger.info(f"Seleccionando equipaje adicional: {weight}kg")
        
        success = self.click(self.EXTRA_BAGGAGE_CHECKBOX, "Checkbox equipaje")
        
        if success:
            time.sleep(0.5)
            if weight == 20:
                success = self.click(self.BAGGAGE_OPTION_20KG, "20kg equipaje")
            elif weight == 30:
                success = self.click(self.BAGGAGE_OPTION_30KG, "30kg equipaje")
        
        return success
    
    @allure.step("Seleccionar asiento preferencial")
    def select_preferential_seat(self):
        """Seleccionar asiento preferencial"""
        logger.info("Seleccionando asiento preferencial")
        return self.click(self.PREFERENTIAL_SEAT_CHECKBOX, "Asiento preferencial")
    
    @allure.step("Seleccionar seguro de viaje")
    def select_travel_insurance(self):
        """Seleccionar seguro de viaje"""
        logger.info("Seleccionando seguro de viaje")
        return self.click(self.TRAVEL_INSURANCE_CHECKBOX, "Seguro de viaje")
    
    @allure.step("Seleccionar priority boarding")
    def select_priority_boarding(self):
        """Seleccionar priority boarding"""
        logger.info("Seleccionando priority boarding")
        return self.click(self.PRIORITY_BOARDING_CHECKBOX, "Priority boarding")
    
    @allure.step("Seleccionar cualquier servicio disponible")
    def select_any_service(self):
        """Seleccionar cualquier servicio disponible"""
        logger.info("Seleccionando cualquier servicio")
        
        # Intentar seleccionar lounge
        if self.select_avianca_lounge():
            return True
        
        # Si no hay lounge, intentar con equipaje
        if self.select_extra_baggage():
            return True
        
        # Si no hay equipaje, intentar con seguro
        if self.select_travel_insurance():
            return True
        
        logger.warning("No se encontraron servicios disponibles")
        return False
    
    @allure.step("Saltar todos los servicios")
    def skip_all_services(self):
        """Saltar todos los servicios adicionales"""
        logger.info("Saltando todos los servicios")
        
        # Intentar click en botón skip si existe
        if self.wait_for_element(self.SKIP_SERVICES_BUTTON, "Botón skip", timeout=3):
            return self.click(self.SKIP_SERVICES_BUTTON, "Saltar servicios")
        
        # Si no hay botón skip, simplemente continuar
        logger.info("No hay botón skip, continuando...")
        return True
    
    @allure.step("Continuar a selección de asientos")
    def continue_to_seatmap(self):
        """Continuar a la página de selección de asientos"""
        logger.info("Continuando a selección de asientos")
        return self.click(self.CONTINUE_BUTTON, "Continuar a asientos")