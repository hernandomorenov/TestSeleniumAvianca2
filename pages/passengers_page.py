from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import allure
import time
import random
from pages.base_page import BasePage
from utils.logger import logger

# Inicializar Faker
fake = Faker()

class PassengersPage(BasePage):
    """Página de información de pasajeros con Faker integrado"""
    
    # ==================== LOCATORS BASADOS EN CSV ====================
    
    # Patrón de IDs dinámicos del CSV:
    # Adulto: 7E7E3533344234383244333232443435353835347E32
    # Joven: 7E7E3533344234383244333132443435353835347E31
    # Niño: 7E7E3533344234383244333332443435353835347E33
    # Infante: 7E7E3533344234383244333432443435353835347E34
    
    # Locators generales (independientes del ID dinámico)
    GENDER_COMBOBOX = (By.XPATH, "//button[contains(@id, 'IdPaxGender_')]")
    GENDER_MALE = (By.XPATH, "//button[contains(text(),'Male')]")
    GENDER_FEMALE = (By.XPATH, "//button[contains(text(),'Female')]")
    
    # Fecha de nacimiento
    DAY_DROPDOWN = (By.XPATH, "//button[contains(@id, 'dateDayId_')]")
    MONTH_DROPDOWN = (By.XPATH, "//button[contains(@id, 'dateMonthId_')]")
    YEAR_DROPDOWN = (By.XPATH, "//button[contains(@id, 'dateYearId_')]")
    
    # Nacionalidad
    NATIONALITY_COMBOBOX = (By.XPATH, "//button[contains(@id, 'IdDocNationality_')]")
    COLOMBIA_OPTION = (By.XPATH, "//button[contains(text(),'Colombia')] | //span[contains(text(),'Colombia')]")
    
    # Programa de cliente
    CUSTOMER_PROGRAM = (By.XPATH, "//button[@id='customerPrograms']")
    NOT_APPLICABLE = (By.XPATH, "//button[contains(text(),'Not applicable')]")
    
    # Campos de texto (nombre, apellido, documento, email, teléfono)
    FIRST_NAME_INPUT = (By.XPATH, "//input[contains(@id, 'firstName') or contains(@name, 'firstName')]")
    LAST_NAME_INPUT = (By.XPATH, "//input[contains(@id, 'lastName') or contains(@name, 'lastName')]")
    DOCUMENT_INPUT = (By.XPATH, "//input[contains(@id, 'IdDocNumber') or contains(@name, 'document')]")
    EMAIL_INPUT = (By.XPATH, "//input[contains(@id, 'email') or contains(@type, 'email')]")
    PHONE_INPUT = (By.XPATH, "//input[contains(@id, 'phone') or contains(@name, 'phone')]")
    
    # Pasajero acompañante (para infante)
    PASSENGER_SELECTOR = (By.ID, "passengerId")
    
    # Prefijo telefónico
    PHONE_PREFIX = (By.ID, "phone_prefixPhoneId")
    PHONE_PREFIX_57 = (By.XPATH, "//span[normalize-space()='57']")
    
    # Newsletter checkbox
    NEWSLETTER_CHECKBOX = (By.ID, "sendNewsLetter")
    
    # Botón Continue
    CONTINUE_BUTTON = (By.XPATH, "//button[@class='button page_button btn-action page_button-primary-flow ng-star-inserted']//span[@class='button_label'][normalize-space()='Continue']")
    
    # ==================== MÉTODOS CON FAKER ====================
    
    def __init__(self, driver):
        """Inicializar con Faker"""
        super().__init__(driver)
        self.fake = Faker()
        self.fake_es = Faker('es_ES')  # Faker en español para nombres más realistas
    
    @allure.step("Generar datos de pasajero con Faker")
    def generate_passenger_data(self, passenger_type="adult"):
        """
        Generar datos aleatorios para un pasajero usando Faker
        
        Args:
            passenger_type: "adult", "youth", "child", o "infant"
        
        Returns:
            dict con todos los datos del pasajero
        """
        # Definir edades según tipo de pasajero
        age_ranges = {
            "adult": (18, 65),
            "youth": (12, 17),
            "child": (2, 11),
            "infant": (0, 1)
        }
        
        age = random.randint(*age_ranges.get(passenger_type, (25, 50)))
        birth_year = 2025 - age
        
        # Generar género aleatorio
        gender = random.choice(["Male", "Female"])
        
        # Generar datos
        if gender == "Male":
            first_name = self.fake_es.first_name_male()
        else:
            first_name = self.fake_es.first_name_female()
        
        last_name = self.fake_es.last_name()
        
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "birth_day": str(random.randint(1, 28)),  # Día 1-28 para evitar problemas
            "birth_month": str(random.randint(1, 12)),
            "birth_year": str(birth_year),
            "document": str(random.randint(10000000, 99999999)),  # Documento de 8 dígitos
            "nationality": "Colombia",
            "customer_program": "Not applicable"
        }
        
        logger.info(f"✓ Datos generados para {passenger_type}: {first_name} {last_name}, {gender}, {data['birth_day']}/{data['birth_month']}/{data['birth_year']}")
        
        return data
    
    @allure.step("Generar datos de contacto con Faker")
    def generate_contact_data(self):
        """Generar datos de contacto usando Faker"""
        data = {
            "email": self.fake.email(),
            "phone": str(random.randint(3000000000, 3999999999)),  # Número colombiano
            "phone_prefix": "57"
        }
        
        logger.info(f"✓ Datos de contacto generados: {data['email']}, +{data['phone_prefix']} {data['phone']}")
        
        return data
    
    @allure.step("Llenar campo de texto con Faker: {field_name}")
    def fill_text_field(self, locator, value, field_name):
        """Llenar un campo de texto"""
        try:
            # Buscar todos los campos que coincidan
            fields = self.driver.find_elements(*locator)
            
            if not fields:
                logger.warning(f"⚠️ Campo {field_name} no encontrado")
                return False
            
            # Buscar el primer campo visible
            for field in fields:
                try:
                    if field.is_displayed() and field.is_enabled():
                        # Scroll al campo
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                            field
                        )
                        time.sleep(0.5)
                        
                        # Limpiar y llenar
                        field.clear()
                        field.send_keys(value)
                        
                        logger.info(f"  ✓ {field_name}: {value}")
                        return True
                except:
                    continue
            
            logger.warning(f"⚠️ No se pudo llenar {field_name}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error llenando {field_name}: {e}")
            return False
    
    @allure.step("Seleccionar opción de dropdown: {field_name}")
    def select_dropdown_option(self, dropdown_locator, option_locator, field_name):
        """Seleccionar una opción de un dropdown"""
        try:
            # Abrir dropdown
            dropdowns = self.driver.find_elements(*dropdown_locator)
            
            dropdown_opened = False
            for dd in dropdowns:
                try:
                    if dd.is_displayed() and dd.is_enabled():
                        # Scroll
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                            dd
                        )
                        time.sleep(0.5)
                        
                        # Click para abrir
                        self.driver.execute_script("arguments[0].click();", dd)
                        dropdown_opened = True
                        time.sleep(0.5)
                        break
                except:
                    continue
            
            if not dropdown_opened:
                logger.warning(f"⚠️ No se pudo abrir dropdown {field_name}")
                return False
            
            # Seleccionar opción
            try:
                option = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(option_locator)
                )
                
                self.driver.execute_script("arguments[0].click();", option)
                logger.info(f"  ✓ {field_name} seleccionado")
                time.sleep(0.5)
                return True
                
            except Exception as e:
                logger.warning(f"⚠️ Opción {field_name} no encontrada: {e}")
                return False
            
        except Exception as e:
            logger.error(f"❌ Error seleccionando {field_name}: {e}")
            return False
    
    @allure.step("Llenar información completa de pasajero con Faker")
    def fill_passenger_with_faker(self, passenger_number=1, passenger_type="adult"):
        """
        Llenar toda la información de un pasajero usando Faker
        
        Args:
            passenger_number: 1, 2, 3, 4
            passenger_type: "adult", "youth", "child", "infant"
        """
        logger.info(f"=== Llenando {passenger_type.upper()} #{passenger_number} con Faker ===")
        
        # Generar datos
        data = self.generate_passenger_data(passenger_type)
        
        success = True
        
        # 1. Género
        try:
            gender_option = self.GENDER_MALE if data["gender"] == "Male" else self.GENDER_FEMALE
            success &= self.select_dropdown_option(
                self.GENDER_COMBOBOX,
                gender_option,
                f"Género {data['gender']}"
            )
        except Exception as e:
            logger.warning(f"⚠️ Error seleccionando género: {e}")
        
        # 2. Fecha de nacimiento
        try:
            # Día
            day_option = (By.XPATH, f"//button[contains(text(),'{data['birth_day']}')]")
            self.select_dropdown_option(self.DAY_DROPDOWN, day_option, f"Día {data['birth_day']}")
            
            # Mes (convertir número a nombre si es necesario)
            month_names = {
                "1": "January", "2": "February", "3": "March", "4": "April",
                "5": "May", "6": "June", "7": "July", "8": "August",
                "9": "September", "10": "October", "11": "November", "12": "December"
            }
            month_name = month_names.get(data['birth_month'], data['birth_month'])
            month_option = (By.XPATH, f"//button[contains(text(),'{month_name}')]")
            self.select_dropdown_option(self.MONTH_DROPDOWN, month_option, f"Mes {month_name}")
            
            # Año
            year_option = (By.XPATH, f"//button[contains(text(),'{data['birth_year']}')]")
            self.select_dropdown_option(self.YEAR_DROPDOWN, year_option, f"Año {data['birth_year']}")
            
        except Exception as e:
            logger.warning(f"⚠️ Error seleccionando fecha de nacimiento: {e}")
        
        # 3. Nombre
        success &= self.fill_text_field(self.FIRST_NAME_INPUT, data["first_name"], "Nombre")
        
        # 4. Apellido
        success &= self.fill_text_field(self.LAST_NAME_INPUT, data["last_name"], "Apellido")
        
        # 5. Documento
        success &= self.fill_text_field(self.DOCUMENT_INPUT, data["document"], "Documento")
        
        # 6. Nacionalidad
        try:
            success &= self.select_dropdown_option(
                self.NATIONALITY_COMBOBOX,
                self.COLOMBIA_OPTION,
                "Nacionalidad Colombia"
            )
        except Exception as e:
            logger.warning(f"⚠️ Error seleccionando nacionalidad: {e}")
        
        # 7. Programa de cliente
        try:
            success &= self.select_dropdown_option(
                self.CUSTOMER_PROGRAM,
                self.NOT_APPLICABLE,
                "Customer Program"
            )
        except Exception as e:
            logger.warning(f"⚠️ Error seleccionando customer program: {e}")
        
        logger.info(f"✅ {passenger_type.upper()} #{passenger_number} completado")
        return success
    
    @allure.step("Llenar información de contacto con Faker")
    def fill_contact_with_faker(self):
        """Llenar información de contacto usando Faker"""
        logger.info("=== Llenando INFORMACIÓN DE CONTACTO con Faker ===")
        
        # Generar datos
        contact_data = self.generate_contact_data()
        
        success = True
        
        # 1. Email
        success &= self.fill_text_field(self.EMAIL_INPUT, contact_data["email"], "Email")
        
        # 2. Prefijo telefónico (+57)
        try:
            self.select_dropdown_option(
                (By.ID, "phone_prefixPhoneId"),
                self.PHONE_PREFIX_57,
                "Prefijo +57"
            )
        except Exception as e:
            logger.warning(f"⚠️ Error seleccionando prefijo: {e}")
        
        # 3. Teléfono
        success &= self.fill_text_field(self.PHONE_INPUT, contact_data["phone"], "Teléfono")
        
        # 4. Newsletter checkbox (opcional)
        try:
            checkbox = self.wait_for_element(self.NEWSLETTER_CHECKBOX, timeout=3)
            if checkbox and not checkbox.is_selected():
                self.driver.execute_script("arguments[0].click();", checkbox)
                logger.info("  ✓ Newsletter checkbox marcado")
        except:
            logger.debug("Newsletter checkbox no encontrado (opcional)")
        
        logger.info("✅ Información de contacto completada")
        return success
    
    @allure.step("Llenar TODOS los pasajeros con Faker")
    def fill_all_passengers_with_faker(self, adults=1, youths=0, children=0, infants=0):
        """
        Llenar todos los pasajeros automáticamente con Faker
        
        Args:
            adults: Cantidad de adultos
            youths: Cantidad de jóvenes
            children: Cantidad de niños
            infants: Cantidad de infantes
        """
        logger.info("="*60)
        logger.info("LLENANDO TODOS LOS PASAJEROS CON FAKER")
        logger.info(f"{adults}A + {youths}Y + {children}C + {infants}I")
        logger.info("="*60)
        
        success = True
        
        # Adultos
        for i in range(adults):
            success &= self.fill_passenger_with_faker(i + 1, "adult")
            time.sleep(1)
        
        # Jóvenes
        for i in range(youths):
            success &= self.fill_passenger_with_faker(i + 1, "youth")
            time.sleep(1)
        
        # Niños
        for i in range(children):
            success &= self.fill_passenger_with_faker(i + 1, "child")
            time.sleep(1)
        
        # Infantes
        for i in range(infants):
            success &= self.fill_passenger_with_faker(i + 1, "infant")
            
            # Seleccionar pasajero acompañante (adulto 1)
            try:
                self.select_dropdown_option(
                    self.PASSENGER_SELECTOR,
                    (By.XPATH, "//button[@role='option'][1]"),
                    "Pasajero acompañante"
                )
            except:
                logger.debug("Selector de acompañante no requerido")
            
            time.sleep(1)
        
        # Información de contacto
        success &= self.fill_contact_with_faker()
        
        logger.info("="*60)
        logger.info(f"{'✅ TODOS LOS PASAJEROS COMPLETADOS' if success else '⚠️ COMPLETADO CON WARNINGS'}")
        logger.info("="*60)
        
        return success
    
    @allure.step("Continuar a servicios")
    def continue_to_services(self):
        """Continuar a la página de servicios"""
        logger.info("Continuando a servicios...")
        
        try:
            # Botón Continue
            continue_btn = self.wait_for_element(self.CONTINUE_BUTTON, timeout=10)
            
            if not continue_btn:
                logger.error("❌ Botón Continue no encontrado")
                return False
            
            # Scroll y click
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                continue_btn
            )
            time.sleep(1)
            
            self.driver.execute_script("arguments[0].click();", continue_btn)
            logger.info("✓ Continue button clicked - Navegando a servicios")
            
            time.sleep(3)
            return True
            
        except Exception as e:
            logger.error(f"Error continuando a servicios: {e}")
            self.take_screenshot("continue_services_error")
            return False