"""
Page Object para información de pasajeros
"""
from selenium.webdriver.common.by import By
import allure
from pages.base_page import BasePage
from utils.logger import logger

class PassengersPage(BasePage):
    """Página de información de pasajeros"""
    
    # ==================== LOCATORS ====================
    
    # Adulto 1
    ADULT1_FIRST_NAME = (By.ID, "adult1-firstname")
    ADULT1_LAST_NAME = (By.ID, "adult1-lastname")
    ADULT1_GENDER = (By.ID, "adult1-gender")
    ADULT1_DOCUMENT = (By.ID, "adult1-document")
    ADULT1_BIRTH_DATE = (By.ID, "adult1-birthdate")
    
    # Joven 1
    YOUTH1_FIRST_NAME = (By.ID, "youth1-firstname")
    YOUTH1_LAST_NAME = (By.ID, "youth1-lastname")
    
    # Niño 1
    CHILD1_FIRST_NAME = (By.ID, "child1-firstname")
    CHILD1_LAST_NAME = (By.ID, "child1-lastname")
    
    # Infante 1
    INFANT1_FIRST_NAME = (By.ID, "infant1-firstname")
    INFANT1_LAST_NAME = (By.ID, "infant1-lastname")
    
    # Contacto
    CONTACT_EMAIL = (By.ID, "contact-email")
    CONTACT_PHONE = (By.ID, "contact-phone")
    
    # Continuar
    CONTINUE_BUTTON = (By.ID, "continue-passengers")
    
    # ==================== MÉTODOS ====================
    
    @allure.step("Completar información del adulto")
    def fill_adult_info(self, adult_number=1, first_name="", last_name="", 
                       gender="Male", document="", birth_date=""):
        """Completar información del adulto"""
        logger.info(f"Completando info adulto {adult_number}")
        
        # Mapear locators según número de adulto
        locators = {
            1: {
                "first_name": self.ADULT1_FIRST_NAME,
                "last_name": self.ADULT1_LAST_NAME,
                "gender": self.ADULT1_GENDER,
                "document": self.ADULT1_DOCUMENT,
                "birth_date": self.ADULT1_BIRTH_DATE
            }
            # Agregar más adultos si es necesario
        }
        
        if adult_number not in locators:
            logger.error(f"Número de adulto no válido: {adult_number}")
            return False
        
        success = True
        
        # Ingresar datos
        if first_name:
            success &= self.enter_text(locators[adult_number]["first_name"], 
                                      first_name, f"Adulto{adult_number} Nombre")
        
        if last_name:
            success &= self.enter_text(locators[adult_number]["last_name"], 
                                      last_name, f"Adulto{adult_number} Apellido")
        
        if gender:
            gender_select = (By.XPATH, f"//select[@id='adult{adult_number}-gender']/option[contains(text(), '{gender}')]")
            success &= self.select_dropdown(locators[adult_number]["gender"], 
                                           gender_select, f"Género {gender}")
        
        if document:
            success &= self.enter_text(locators[adult_number]["document"], 
                                      document, f"Adulto{adult_number} Documento")
        
        return success
    
    @allure.step("Completar información del joven")
    def fill_youth_info(self, youth_number=1, first_name="", last_name=""):
        """Completar información del joven"""
        logger.info(f"Completando info joven {youth_number}")
        
        success = True
        
        if first_name:
            success &= self.enter_text(self.YOUTH1_FIRST_NAME, 
                                      first_name, f"Joven{youth_number} Nombre")
        
        if last_name:
            success &= self.enter_text(self.YOUTH1_LAST_NAME, 
                                      last_name, f"Joven{youth_number} Apellido")
        
        return success
    
    @allure.step("Completar información del niño")
    def fill_child_info(self, child_number=1, first_name="", last_name=""):
        """Completar información del niño"""
        logger.info(f"Completando info niño {child_number}")
        
        success = True
        
        if first_name:
            success &= self.enter_text(self.CHILD1_FIRST_NAME, 
                                      first_name, f"Niño{child_number} Nombre")
        
        if last_name:
            success &= self.enter_text(self.CHILD1_LAST_NAME, 
                                      last_name, f"Niño{child_number} Apellido")
        
        return success
    
    @allure.step("Completar información del infante")
    def fill_infant_info(self, infant_number=1, first_name="", last_name=""):
        """Completar información del infante"""
        logger.info(f"Completando info infante {infant_number}")
        
        success = True
        
        if first_name:
            success &= self.enter_text(self.INFANT1_FIRST_NAME, 
                                      first_name, f"Infante{infant_number} Nombre")
        
        if last_name:
            success &= self.enter_text(self.INFANT1_LAST_NAME, 
                                      last_name, f"Infante{infant_number} Apellido")
        
        return success
    
    @allure.step("Completar información de contacto")
    def fill_contact_info(self, email="", phone=""):
        """Completar información de contacto"""
        logger.info("Completando info de contacto")
        
        success = True
        
        if email:
            success &= self.enter_text(self.CONTACT_EMAIL, email, "Email contacto")
        
        if phone:
            success &= self.enter_text(self.CONTACT_PHONE, phone, "Teléfono contacto")
        
        return success
    
    @allure.step("Completar información de todos los pasajeros")
    def fill_all_passengers_info(self, passenger_data):
        """Completar información de todos los pasajeros"""
        logger.info("Completando info de todos los pasajeros")
        
        success = True
        
        # Adulto
        if "adult" in passenger_data:
            success &= self.fill_adult_info(
                adult_number=1,
                first_name=passenger_data.get("adult", {}).get("first_name", ""),
                last_name=passenger_data.get("adult", {}).get("last_name", ""),
                gender=passenger_data.get("adult", {}).get("gender", "Male"),
                document=passenger_data.get("adult", {}).get("document", ""),
                birth_date=passenger_data.get("adult", {}).get("birth_date", "")
            )
        
        # Joven
        if "youth" in passenger_data:
            success &= self.fill_youth_info(
                youth_number=1,
                first_name=passenger_data.get("youth", {}).get("first_name", ""),
                last_name=passenger_data.get("youth", {}).get("last_name", "")
            )
        
        # Niño
        if "child" in passenger_data:
            success &= self.fill_child_info(
                child_number=1,
                first_name=passenger_data.get("child", {}).get("first_name", ""),
                last_name=passenger_data.get("child", {}).get("last_name", "")
            )
        
        # Infante
        if "infant" in passenger_data:
            success &= self.fill_infant_info(
                infant_number=1,
                first_name=passenger_data.get("infant", {}).get("first_name", ""),
                last_name=passenger_data.get("infant", {}).get("last_name", "")
            )
        
        # Contacto
        if "contact" in passenger_data:
            success &= self.fill_contact_info(
                email=passenger_data.get("contact", {}).get("email", ""),
                phone=passenger_data.get("contact", {}).get("phone", "")
            )
        
        return success
    
    @allure.step("Continuar a servicios")
    def continue_to_services(self):
        """Continuar a la página de servicios"""
        logger.info("Continuando a servicios")
        return self.click(self.CONTINUE_BUTTON, "Continuar a servicios")