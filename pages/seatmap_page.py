"""
Page Object para selección de asientos
"""
from selenium.webdriver.common.by import By
import allure
import time
from pages.base_page import BasePage
from utils.logger import logger

class SeatmapPage(BasePage):
    """Página de selección de asientos"""
    
    # ==================== LOCATORS ====================
    
    # Mapa de asientos
    SEATMAP_CONTAINER = (By.ID, "seatmap-container")
    
    # Tipos de asientos
    ECONOMY_SEAT = (By.XPATH, "//div[contains(@class, 'seat-economy') and contains(@class, 'available')][1]")
    PLUS_SEAT = (By.XPATH, "//div[contains(@class, 'seat-plus') and contains(@class, 'available')][1]")
    PREMIUM_SEAT = (By.XPATH, "//div[contains(@class, 'seat-premium') and contains(@class, 'available')][1]")
    BUSINESS_SEAT = (By.XPATH, "//div[contains(@class, 'seat-business') and contains(@class, 'available')][1]")
    
    # Botones de acción
    AUTO_SELECT_BUTTON = (By.XPATH, "//button[contains(text(), 'Auto-select')]")
    CONFIRM_SEATS_BUTTON = (By.ID, "confirm-seats")
    SKIP_SEATS_BUTTON = (By.XPATH, "//button[contains(text(), 'Skip seats')]")
    
    # Información de asientos
    SELECTED_SEATS_INFO = (By.CLASS_NAME, "selected-seats")
    
    # ==================== MÉTODOS ====================
    
    @allure.step("Esperar a que cargue el mapa de asientos")
    def wait_for_seatmap(self, timeout=10):
        """Esperar a que cargue el mapa de asientos"""
        logger.info("Esperando carga del mapa de asientos")
        return self.wait_for_element(self.SEATMAP_CONTAINER, "Mapa de asientos", timeout)
    
    @allure.step("Seleccionar asiento tipo: {seat_type}")
    def select_seat_type(self, seat_type="economy"):
        """Seleccionar un asiento por tipo"""
        logger.info(f"Seleccionando asiento tipo: {seat_type}")
        
        seat_locators = {
            "economy": self.ECONOMY_SEAT,
            "plus": self.PLUS_SEAT,
            "premium": self.PREMIUM_SEAT,
            "business": self.BUSINESS_SEAT
        }
        
        if seat_type.lower() not in seat_locators:
            logger.error(f"Tipo de asiento no válido: {seat_type}")
            return False
        
        # Esperar a que cargue el mapa
        if not self.wait_for_seatmap():
            return False
        
        # Intentar seleccionar el asiento
        success = self.click(seat_locators[seat_type.lower()], f"Asiento {seat_type}")
        
        if not success:
            logger.warning(f"No se encontró asiento {seat_type} disponible")
            
            # Intentar auto-selección
            if self.wait_for_element(self.AUTO_SELECT_BUTTON, "Auto-select", timeout=3):
                logger.info("Usando auto-selección")
                return self.click(self.AUTO_SELECT_BUTTON, "Auto-selectar asientos")
        
        return success
    
    @allure.step("Seleccionar múltiples tipos de asientos")
    def select_multiple_seat_types(self, seat_types):
        """Seleccionar múltiples tipos de asientos"""
        logger.info(f"Seleccionando tipos de asientos: {seat_types}")
        
        success = True
        
        for seat_type in seat_types:
            # Esperar un momento entre selecciones
            time.sleep(1)
            
            # Seleccionar asiento
            seat_success = self.select_seat_type(seat_type)
            
            if not seat_success:
                logger.warning(f"No se pudo seleccionar asiento {seat_type}")
                # Continuar con el siguiente aunque falle este
            
            success = success and seat_success
        
        return success
    
    @allure.step("Usar auto-selección de asientos")
    def use_auto_select(self):
        """Usar la función de auto-selección de asientos"""
        logger.info("Usando auto-selección de asientos")
        
        if self.wait_for_element(self.AUTO_SELECT_BUTTON, "Auto-select", timeout=5):
            return self.click(self.AUTO_SELECT_BUTTON, "Auto-select")
        
        logger.warning("No se encontró botón de auto-selección")
        return False
    
    @allure.step("Saltar selección de asientos")
    def skip_seat_selection(self):
        """Saltar la selección de asientos"""
        logger.info("Saltando selección de asientos")
        
        if self.wait_for_element(self.SKIP_SEATS_BUTTON, "Skip seats", timeout=5):
            return self.click(self.SKIP_SEATS_BUTTON, "Saltar asientos")
        
        logger.warning("No se encontró botón para saltar asientos")
        return False
    
    @allure.step("Confirmar selección de asientos")
    def confirm_seats(self):
        """Confirmar la selección de asientos"""
        logger.info("Confirmando selección de asientos")
        return self.click(self.CONFIRM_SEATS_BUTTON, "Confirmar asientos")
    
    @allure.step("Continuar a pagos")
    def continue_to_payments(self):
        """Continuar a la página de pagos"""
        logger.info("Continuando a pagos")
        
        # Primero confirmar asientos si está disponible
        if self.wait_for_element(self.CONFIRM_SEATS_BUTTON, "Confirmar", timeout=3):
            return self.confirm_seats()
        
        # Si no hay confirmación, verificar si hay botón de continuar genérico
        continue_button = (By.XPATH, "//button[contains(text(), 'Continue') or contains(text(), 'Continuar')]")
        if self.wait_for_element(continue_button, "Continuar", timeout=3):
            return self.click(continue_button, "Continuar")
        
        logger.warning("No se encontró botón para continuar")
        return False
    
    @allure.step("Verificar asientos seleccionados")
    def verify_selected_seats(self):
        """Verificar información de asientos seleccionados"""
        try:
            seats_info = self.wait_for_element(self.SELECTED_SEATS_INFO, "Info asientos", timeout=5)
            if seats_info:
                seats_text = seats_info.text
                logger.info(f"Asientos seleccionados: {seats_text}")
                return seats_text
            return None
        except Exception as e:
            logger.error(f"Error verificando asientos: {e}")
            return None