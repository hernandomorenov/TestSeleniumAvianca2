"""
Page Object para página de pagos
"""
from selenium.webdriver.common.by import By
import allure
import time
from pages.base_page import BasePage
from utils.logger import logger

class PaymentsPage(BasePage):
    """Página de pagos"""
    
    # ==================== LOCATORS ====================
    
    # Métodos de pago
    CREDIT_CARD_OPTION = (By.ID, "credit-card-payment")
    DEBIT_CARD_OPTION = (By.ID, "debit-card-payment")
    
    # Información de tarjeta
    CARD_NUMBER = (By.ID, "card-number")
    CARD_HOLDER = (By.ID, "card-holder")
    EXPIRY_MONTH = (By.ID, "expiry-month")
    EXPIRY_YEAR = (By.ID, "expiry-year")
    CVV = (By.ID, "cvv")
    
    # Información de facturación
    BILLING_ADDRESS = (By.ID, "billing-address")
    BILLING_CITY = (By.ID, "billing-city")
    BILLING_ZIP = (By.ID, "billing-zip")
    BILLING_COUNTRY = (By.ID, "billing-country")
    
    # Términos y condiciones
    TERMS_CHECKBOX = (By.ID, "terms-checkbox")
    
    # Botones
    PAY_NOW_BUTTON = (By.ID, "pay-now-button")
    CANCEL_PAYMENT = (By.XPATH, "//button[contains(text(), 'Cancel')]")
    
    # Resumen de pago
    PAYMENT_SUMMARY = (By.CLASS_NAME, "payment-summary")
    TOTAL_AMOUNT = (By.CLASS_NAME, "total-amount")
    
    # Mensajes
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(text(), 'success') or contains(text(), 'éxito')]")
    ERROR_MESSAGE = (By.XPATH, "//div[contains(text(), 'error') or contains(text(), 'rechaz')]")
    
    # ==================== MÉTODOS ====================
    
    @allure.step("Seleccionar pago con tarjeta de crédito")
    def select_credit_card_payment(self):
        """Seleccionar pago con tarjeta de crédito"""
        logger.info("Seleccionando pago con tarjeta de crédito")
        return self.click(self.CREDIT_CARD_OPTION, "Tarjeta de crédito")
    
    @allure.step("Completar información de tarjeta")
    def fill_card_info(self, card_data):
        """Completar información de tarjeta"""
        logger.info("Completando información de tarjeta")
        
        success = True
        
        # Número de tarjeta
        if "card_number" in card_data:
            success &= self.enter_text(self.CARD_NUMBER, 
                                      card_data["card_number"], 
                                      "Número de tarjeta")
        
        # Nombre del titular
        if "card_holder" in card_data:
            success &= self.enter_text(self.CARD_HOLDER, 
                                      card_data["card_holder"], 
                                      "Titular de tarjeta")
        
        # Mes de expiración
        if "expiry_month" in card_data:
            month_option = (By.XPATH, f"//select[@id='expiry-month']/option[@value='{card_data['expiry_month']}']")
            success &= self.select_dropdown(self.EXPIRY_MONTH, 
                                           month_option, 
                                           f"Mes {card_data['expiry_month']}")
        
        # Año de expiración
        if "expiry_year" in card_data:
            year_option = (By.XPATH, f"//select[@id='expiry-year']/option[contains(text(), '{card_data['expiry_year']}')]")
            success &= self.select_dropdown(self.EXPIRY_YEAR, 
                                           year_option, 
                                           f"Año {card_data['expiry_year']}")
        
        # CVV
        if "cvv" in card_data:
            success &= self.enter_text(self.CVV, 
                                      card_data["cvv"], 
                                      "CVV")
        
        return success
    
    @allure.step("Completar información de facturación")
    def fill_billing_info(self, billing_data):
        """Completar información de facturación"""
        logger.info("Completando información de facturación")
        
        success = True
        
        # Dirección
        if "address" in billing_data:
            success &= self.enter_text(self.BILLING_ADDRESS, 
                                      billing_data["address"], 
                                      "Dirección")
        
        # Ciudad
        if "city" in billing_data:
            success &= self.enter_text(self.BILLING_CITY, 
                                      billing_data["city"], 
                                      "Ciudad")
        
        # Código postal
        if "zip" in billing_data:
            success &= self.enter_text(self.BILLING_ZIP, 
                                      billing_data["zip"], 
                                      "Código postal")
        
        # País
        if "country" in billing_data:
            country_option = (By.XPATH, f"//select[@id='billing-country']/option[contains(text(), '{billing_data['country']}')]")
            success &= self.select_dropdown(self.BILLING_COUNTRY, 
                                           country_option, 
                                           f"País {billing_data['country']}")
        
        return success
    
    @allure.step("Aceptar términos y condiciones")
    def accept_terms(self):
        """Aceptar términos y condiciones"""
        logger.info("Aceptando términos y condiciones")
        return self.click(self.TERMS_CHECKBOX, "Términos y condiciones")
    
    @allure.step("Realizar pago")
    def submit_payment(self):
        """Realizar el pago"""
        logger.info("Realizando pago")
        
        # Aceptar términos primero
        self.accept_terms()
        time.sleep(0.5)
        
        # Realizar pago
        return self.click(self.PAY_NOW_BUTTON, "Pagar ahora")
    
    @allure.step("Cancelar pago")
    def cancel_payment(self):
        """Cancelar el proceso de pago"""
        logger.info("Cancelando pago")
        return self.click(self.CANCEL_PAYMENT, "Cancelar pago")
    
    @allure.step("Completar información de pago pero no enviar")
    def fill_payment_but_not_submit(self, card_data, billing_data=None):
        """Completar información de pago pero no enviar"""
        logger.info("Completando info de pago sin enviar")
        
        success = True
        
        # Seleccionar tarjeta de crédito
        success &= self.select_credit_card_payment()
        
        # Completar info de tarjeta
        success &= self.fill_card_info(card_data)
        
        # Completar info de facturación si se proporciona
        if billing_data:
            success &= self.fill_billing_info(billing_data)
        
        # Aceptar términos
        success &= self.accept_terms()
        
        # NO hacer click en "Pagar ahora"
        # Solo verificar que el botón está disponible
        if success:
            pay_button = self.wait_for_element(self.PAY_NOW_BUTTON, "Botón pagar", timeout=5)
            if pay_button and pay_button.is_enabled():
                logger.info("✅ Información de pago completada (no enviada)")
                return True
        
        return False
    
    @allure.step("Verificar resumen de pago")
    def verify_payment_summary(self):
        """Verificar el resumen de pago"""
        try:
            summary = self.wait_for_element(self.PAYMENT_SUMMARY, "Resumen de pago", timeout=5)
            if summary:
                summary_text = summary.text
                logger.info(f"Resumen de pago: {summary_text}")
                return summary_text
            
            # También verificar el total
            total = self.wait_for_element(self.TOTAL_AMOUNT, "Total a pagar", timeout=5)
            if total:
                total_text = total.text
                logger.info(f"Total a pagar: {total_text}")
                return total_text
            
            return None
            
        except Exception as e:
            logger.error(f"Error verificando resumen: {e}")
            return None
    
    @allure.step("Verificar mensaje de éxito/error")
    def verify_payment_message(self):
        """Verificar mensaje de pago"""
        try:
            # Verificar mensaje de éxito
            success_msg = self.wait_for_element(self.SUCCESS_MESSAGE, "Mensaje éxito", timeout=10)
            if success_msg:
                logger.info(f"Mensaje de éxito: {success_msg.text}")
                return "success"
            
            # Verificar mensaje de error
            error_msg = self.wait_for_element(self.ERROR_MESSAGE, "Mensaje error", timeout=10)
            if error_msg:
                logger.info(f"Mensaje de error: {error_msg.text}")
                return "error"
            
            logger.warning("No se encontró mensaje de pago")
            return None
            
        except Exception as e:
            logger.error(f"Error verificando mensaje: {e}")
            return None