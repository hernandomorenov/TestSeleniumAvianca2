import pytest
import allure
import time
from faker import Faker
from utils.config import Config
from utils.logger import logger
from pages.home_page import HomePage
from pages.flight_selection_page import FlightSelectionPage
from pages.passengers_page import PassengersPage
from pages.services_page import ServicesPage
from pages.seatmap_page import SeatmapPage
from pages.payments_page import PaymentsPage


fake = Faker()


@allure.epic("Avianca Booking Automation")
@allure.feature("Booking Flow - One Way")
@allure.story("Caso 1: Booking One-way con todos los tipos de pasajeros")
@pytest.mark.caso_1
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.booking
class TestCase1OneWay:
    """Caso automatizado 1: Realizar booking One-way (Solo ida)"""

    @allure.title("Caso 1: One-way booking con validaciones completas")
    @allure.description("""
    Test completo de booking one-way cumpliendo todos los requisitos:
    1. Home: Idioma, POS, origen, destino, 1 pasajero de cada tipo
    2. Flight Selection: Tarifa Basic
    3. Passengers: Información completa de 4 pasajeros
    4. Services: No seleccionar ninguno
    5. Seatmap: Asiento economy
    6. Payments: Pago con tarjeta fake
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("booking", "one-way", "complete-flow", "requisitos", "15pts")
    def test_one_way_booking_complete(self, driver, setup_test):
        """Test principal del caso 1 - Booking One-way"""
        self._initialize_pages(driver)
        self._setup_test_environment(setup_test, driver)
        
        # Ejecutar todos los pasos del flujo de booking
        self._execute_home_page_steps()
        self._execute_flight_selection_steps()
        self._execute_passengers_steps()
        self._execute_services_steps()
        self._execute_seatmap_steps()
        self._execute_payments_steps()
        
        # Verificación final
        self._generate_final_report(driver)

    # ==================== MÉTODOS PRIVADOS ====================

    def _initialize_pages(self, driver):
        """Inicializar todos los Page Objects"""
        self.home_page = HomePage(driver)
        self.flight_page = FlightSelectionPage(driver)
        self.passengers_page = PassengersPage(driver)
        self.services_page = ServicesPage(driver)
        self.seatmap_page = SeatmapPage(driver)
        self.payments_page = PaymentsPage(driver)
        
        logger.info("✅ Page Objects inicializados correctamente")

    def _setup_test_environment(self, setup_test, driver):
        """Configurar el entorno inicial del test"""
        with allure.step("Configuración inicial del test"):
            self.browser_name = driver.capabilities.get('browserName', 'chrome')
            self.base_url = setup_test
            
            allure.attach(
                f"Browser: {self.browser_name}\nURL: {self.base_url}",
                name="Información del Test",
                attachment_type=allure.attachment_type.TEXT
            )
            
            logger.info(f"🛠  Browser: {self.browser_name}")
            logger.info(f"🌐 URL Base: {self.base_url}")

    def _execute_home_page_steps(self):
        """Ejecutar los pasos de la página Home"""
        with allure.step("REQUISITO 1: HOME PAGE - Configuración inicial"):
            logger.info("="*60)
            logger.info("REQUISITO 1: CONFIGURACIÓN HOME PAGE")
            logger.info("="*60)
            
            # 1. Navegar a la página
            assert self.home_page.navigate_to(self.base_url), \
                "❌ No se pudo navegar a la página"
            
            time.sleep(3)
            self.home_page.take_screenshot("01_home_inicio")
            
            # 2. Configurar idioma, POS, origen, destino y pasajeros
            success = self.home_page.complete_home_configuration(
                language="English",
                pos="Colombia",
                origin_city="Bogota",
                origin_code="BOG",
                dest_city="Medellin",
                dest_code="MDE",
                day=None  # Fecha automática: 2 días después de hoy
            )
            
            assert success, "❌ No se pudo completar configuración home"
            
            logger.info("✅ REQUISITO 1 COMPLETADO: Configuración home exitosa")
            self.home_page.take_screenshot("01_home_completado")

    def _execute_flight_selection_steps(self):
        """Ejecutar los pasos de selección de vuelo"""
        with allure.step("REQUISITO 2: FLIGHT SELECTION - Seleccionar tarifa Basic"):
            logger.info("="*60)
            logger.info("REQUISITO 2: SELECCIÓN DE VUELO")
            logger.info("="*60)
            
            # 1. Esperar carga de página
            assert self.flight_page.wait_for_page_load(), \
                "❌ Página de vuelos no cargó"
            
            self.home_page.take_screenshot("02_flights_cargado")
            
            # 2. Seleccionar tarifa Basic
            assert self.flight_page.select_fare(fare_type="Basic"), \
                "❌ No se pudo seleccionar tarifa Basic"
            
            # 3. Verificar precio
            price = self.flight_page.verify_flight_price()
            if price:
                allure.attach(f"Precio: {price}", "Precio Vuelo", 
                            allure.attachment_type.TEXT)
            
            # 4. Continuar
            assert self.flight_page.continue_to_passengers(), \
                "❌ No se pudo continuar a pasajeros"
            
            logger.info("✅ REQUISITO 2 COMPLETADO: Tarifa Basic seleccionada")
            time.sleep(3)

    def _generate_passenger_data(self):
        """Generar datos fake para los pasajeros"""
        return {
            "adult": {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "gender": "Male",
                "document": str(fake.random_number(digits=10)),
                "birth_date": "01/01/1990"
            },
            "youth": {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "gender": "Female",
                "document": str(fake.random_number(digits=10)),
                "birth_date": "15/05/2006"
            },
            "child": {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "gender": "Male",
                "document": str(fake.random_number(digits=10)),
                "birth_date": "20/08/2015",
                "birth_certificate": "CERT-12345"
            },
            "infant": {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "gender": "Female",
                "birth_date": "10/03/2023",
                "adult_accompanying": "1"
            },
            "contact": {
                "email": fake.email(),
                "phone": "1234567890",
                "country": "Colombia"
            }
        }

    def _execute_passengers_steps(self):
        """Ejecutar los pasos de información de pasajeros"""
        with allure.step("REQUISITO 3: PASSENGERS - Ingresar información"):
            logger.info("="*60)
            logger.info("REQUISITO 3: INFORMACIÓN DE PASAJEROS")
            logger.info("="*60)
            
            # 1. Esperar carga de página
            assert self.passengers_page.wait_for_page_load(), \
                "❌ Página de pasajeros no cargó"
            
            self.home_page.take_screenshot("03_passengers_cargado")
            
            # 2. Generar datos
            passenger_data = self._generate_passenger_data()
            
            # 3. Llenar información
            assert self.passengers_page.fill_all_passengers_info(passenger_data), \
                "❌ No se pudo completar información de pasajeros"
            
            self.home_page.take_screenshot("03_passengers_completado")
            
            # 4. Continuar
            assert self.passengers_page.continue_to_services(), \
                "❌ No se pudo continuar a servicios"
            
            logger.info("✅ REQUISITO 3 COMPLETADO: Información de pasajeros ingresada")
            time.sleep(3)

    def _execute_services_steps(self):
        """Ejecutar los pasos de servicios adicionales"""
        with allure.step("REQUISITO 4: SERVICES - No seleccionar servicios"):
            logger.info("="*60)
            logger.info("REQUISITO 4: SERVICIOS ADICIONALES")
            logger.info("="*60)
            
            # 1. Esperar carga de página
            assert self.services_page.wait_for_page_load(), \
                "❌ Página de servicios no cargó"
            
            self.home_page.take_screenshot("04_services_cargado")
            
            # 2. Saltar servicios
            assert self.services_page.skip_all_services(), \
                "❌ No se pudo saltar servicios"
            
            # 3. Continuar
            assert self.services_page.continue_to_seatmap(), \
                "❌ No se pudo continuar a asientos"
            
            logger.info("✅ REQUISITO 4 COMPLETADO: Ningún servicio seleccionado")
            time.sleep(3)

    def _execute_seatmap_steps(self):
        """Ejecutar los pasos de selección de asientos"""
        with allure.step("REQUISITO 5: SEATMAP - Seleccionar asiento economy"):
            logger.info("="*60)
            logger.info("REQUISITO 5: SELECCIÓN DE ASIENTOS")
            logger.info("="*60)
            
            # 1. Esperar carga de página
            assert self.seatmap_page.wait_for_page_load(), \
                "❌ Página de asientos no cargó"
            
            self.home_page.take_screenshot("05_seatmap_cargado")
            
            # 2. Esperar mapa de asientos
            assert self.seatmap_page.wait_for_seatmap(), \
                "❌ Mapa de asientos no cargó"
            
            # 3. Seleccionar asiento economy
            assert self.seatmap_page.select_seat_type("economy"), \
                "❌ No se pudo seleccionar asiento economy"
            
            # 4. Verificar asientos
            seats_info = self.seatmap_page.verify_selected_seats()
            if seats_info:
                allure.attach(f"Asientos: {seats_info}", "Asientos Seleccionados",
                            allure.attachment_type.TEXT)
            
            self.home_page.take_screenshot("05_seatmap_completado")
            
            # 5. Continuar
            assert self.seatmap_page.continue_to_payments(), \
                "❌ No se pudo continuar a pagos"
            
            logger.info("✅ REQUISITO 5 COMPLETADO: Asiento economy seleccionado")
            time.sleep(3)

    def _generate_payment_data(self):
        """Generar datos para el pago"""
        return {
            "card": {
                "card_number": "4242424242424242",
                "card_holder": fake.name(),
                "expiry_month": "12",
                "expiry_year": "2025",
                "cvv": "123"
            },
            "billing": {
                "address": fake.street_address(),
                "city": fake.city(),
                "zip": "110111",
                "country": "Colombia"
            }
        }

    def _execute_payments_steps(self):
        """Ejecutar los pasos de pago"""
        with allure.step("REQUISITO 6: PAYMENTS - Pago con tarjeta fake"):
            logger.info("="*60)
            logger.info("REQUISITO 6: PROCESO DE PAGO")
            logger.info("="*60)
            
            # 1. Esperar carga de página
            assert self.payments_page.wait_for_page_load(), \
                "❌ Página de pagos no cargó"
            
            self.home_page.take_screenshot("06_payments_cargado")
            
            # 2. Generar datos de pago
            payment_data = self._generate_payment_data()
            
            # 3. Verificar resumen
            summary = self.payments_page.verify_payment_summary()
            if summary:
                allure.attach(f"Resumen: {summary}", "Resumen de Pago",
                            allure.attachment_type.TEXT)
            
            # 4. Completar formulario de pago
            assert self.payments_page.fill_card_info(payment_data["card"]), \
                "❌ No se pudo completar info de tarjeta"
            
            assert self.payments_page.fill_billing_info(payment_data["billing"]), \
                "❌ No se pudo completar info de facturación"
            
            assert self.payments_page.accept_terms(), \
                "❌ No se pudo aceptar términos"
            
            self.home_page.take_screenshot("06_payments_formulario_completado")
            
            # 5. Realizar pago
            payment_success = self.payments_page.submit_payment()
            
            # 6. Verificar estado
            self.payment_status = self.payments_page.verify_payment_message()
            allure.attach(f"Estado: {self.payment_status or 'No verificado'}",
                        "Estado del Pago", allure.attachment_type.TEXT)
            
            logger.info("✅ REQUISITO 6 COMPLETADO: Pago con tarjeta fake procesado")
            self.home_page.take_screenshot("06_payments_procesado")

    def _generate_final_report(self, driver):
        """Generar reporte final del test"""
        with allure.step("📋 VERIFICACIÓN FINAL - Todos los requisitos completados"):
            logger.info("="*80)
            logger.info("VERIFICACIÓN FINAL - RESUMEN DEL TEST")
            logger.info("="*80)
            
            self.home_page.take_screenshot("07_test_completado")
            
            report = self._create_test_report(driver)
            allure.attach(report, "📋 Resumen Completo - Caso 1 (15 Pts)",
                         allure.attachment_type.TEXT)
            
            logger.info(report)
            logger.info("✅✅✅ CASO 1 COMPLETADO EXITOSAMENTE ✅✅✅")

    def _create_test_report(self, driver):
        """Crear reporte estructurado del test"""
        return f"""
        ==================== CASO 1: BOOKING ONE-WAY ====================
        
        ✅ REQUISITO 1: HOME PAGE
           • Idioma: English
           • POS: Colombia
           • Origen: Bogota (BOG)
           • Destino: Medellin (MDE)
           • Pasajeros: 1 Adulto, 1 Joven, 1 Niño, 1 Infante
        
        ✅ REQUISITO 2: FLIGHT SELECTION
           • Tarifa: Basic seleccionada
        
        ✅ REQUISITO 3: PASSENGERS
           • Información completa de 4 tipos de pasajeros
           • Datos generados automáticamente con Faker
        
        ✅ REQUISITO 4: SERVICES
           • Ningún servicio seleccionado (según requisitos)
        
        ✅ REQUISITO 5: SEATMAP
           • Asiento economy seleccionado
        
        ✅ REQUISITO 6: PAYMENTS
           • Pago con tarjeta fake procesado
           • Estado: {self.payment_status or 'Procesado'}
           • Importante: No importa si el pago es rechazado
        
        ==================== INFORMACIÓN DEL TEST ====================
        • Browser: {self.browser_name}
        • URL Base: {self.base_url}
        • URL Final: {driver.current_url}
        • Título: {driver.title}
        • Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}
        
        ==================== RESULTADO ====================
        ✅ TEST COMPLETADO EXITOSAMENTE - TODOS LOS REQUISITOS CUMPLIDOS
        ================================================================
        """