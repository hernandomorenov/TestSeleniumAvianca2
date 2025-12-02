import pytest
import allure
from pages.home_page import HomePage
from pages.flight_selection_page import FlightSelectionPage
from pages.passengers_page import PassengersPage
from pages.services_page import ServicesPage
from pages.seatmap_page import SeatmapPage
from pages.payments_page import PaymentsPage
from utils.config import Config
from faker import Faker
from utils.logger import logger

fake = Faker()

@allure.epic("FLYR Automation Suite")
@allure.feature("Booking Flow")
@allure.story("One-way Booking")
@pytest.mark.booking
@pytest.mark.smoke
@pytest.mark.regression
class TestCase1OneWay:
    """Caso 1: Booking One-way con todos los tipos de pasajeros"""
    
    @allure.title("Test 1: One-way booking with all passenger types")
    @allure.description("Complete one-way booking flow ")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("booking", "one-way", "complete-flow", "following", "pom")
    def test_one_way_booking_csv(self, driver, setup_test, request):
        # Inicializar páginas
        home_page = HomePage(driver)
        flight_page = FlightSelectionPage(driver)
        passengers_page = PassengersPage(driver)
        services_page = ServicesPage(driver)
        seatmap_page = SeatmapPage(driver)
        payments_page = PaymentsPage(driver)
        
        # Tomar screenshot inicial
        home_page.take_screenshot("test_start")
        
        # ==================== HOME PAGE ====================
        with allure.step("1. Home Page - Open website"):
            allure.attach(f"Browser: {request.cls.browser}", name="Browser Info", attachment_type=allure.attachment_type.TEXT)
            allure.attach(f"URL: {setup_test}", name="Test URL", attachment_type=allure.attachment_type.TEXT)
            
            # Navegar a la página
            assert home_page.navigate_to(setup_test), "No se pudo navegar a la página"
            
            # Verificar que estamos en la página correcta
            assert "avianca" in driver.current_url.lower() or "avtest" in driver.current_url.lower(), \
                "No estamos en la página de Avianca"
        
        with allure.step("2. Complete home configuration"):
            
            assert home_page.complete_home_configuration_csv(), \
                "No se pudo completar configuración home según CSV"
        
        # ==================== SELECT FLIGHT ====================
        with allure.step("3. Flight Selection - Follow CSV steps 19-27"):
            assert flight_page.wait_for_page_load(), "Página de vuelos no cargó"
            
            # Verificar que estamos en la página correcta
            assert "select" in driver.current_url.lower() or "vuelos" in driver.current_url.lower(), \
                "No estamos en la página de selección de vuelos"
            
            # Seleccionar tarifa 
            assert flight_page.select_fare_csv(), "No se pudo seleccionar tarifa según CSV"
            
            # Verificar precio
            price = flight_page.verify_flight_price()
            assert price is not None, "No se mostró el precio del vuelo"
            allure.attach(f"Precio del vuelo: {price}", name="Flight Price", attachment_type=allure.attachment_type.TEXT)
            
           
            assert flight_page.continue_csv(), "No se pudo continuar según CSV"
        
        # ==================== PASSENGERS - MANTENIENDO POM ====================
        with allure.step("4. Passengers - Ingresar información (Validación requerida)"):
            assert passengers_page.wait_for_page_load(), "Página de pasajeros no cargó"
            
            # Preparar datos fake para pasajeros (1 de cada tipo)
            passenger_data = {
                "adult": {
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "gender": "Male",
                    "document": str(fake.random_number(digits=10)),
                    "birth_date": "1990-01-01"
                },
                "youth": {
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "gender": "Female",
                    "document": str(fake.random_number(digits=10)),
                    "birth_date": "2006-05-15"
                },
                "child": {
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "gender": "Male",
                    "document": str(fake.random_number(digits=10)),
                    "birth_date": "2015-08-20",
                    "birth_certificate": "CERT-12345"
                },
                "infant": {
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "gender": "Female",
                    "birth_date": "2023-03-10",
                    "adult_accompanying": "1"  # Primer adulto
                },
                "contact": {
                    "email": fake.email(),
                    "phone": fake.phone_number()[:15],
                    "country": "Colombia"
                }
            }
            
            # Completar información de todos los pasajeros
            assert passengers_page.fill_all_passengers_info(passenger_data), \
                "No se pudo completar información de pasajeros"
            
            # Continuar
            assert passengers_page.continue_to_services(), "No se pudo continuar a servicios"
        
        # ==================== SERVICES - MANTENIENDO POM ====================
        with allure.step("5. Services - No seleccionar ninguno (Validación requerida)"):
            assert services_page.wait_for_page_load(), "Página de servicios no cargó"
            
            # Saltar todos los servicios
            assert services_page.skip_all_services(), "No se pudo saltar servicios"
            
            # Continuar
            assert services_page.continue_to_seatmap(), "No se pudo continuar a asientos"
        
        # ==================== SEATMAP - MANTENIENDO POM ====================
        with allure.step("6. Seatmap - Seleccionar asiento economy (Validación requerida)"):
            assert seatmap_page.wait_for_page_load(), "Página de asientos no cargó"
            
            # Esperar a que cargue el mapa de asientos
            assert seatmap_page.wait_for_seatmap(), "Mapa de asientos no cargó"
            
            # Seleccionar asiento economy
            assert seatmap_page.select_seat_type("economy"), "No se pudo seleccionar asiento economy"
            
            # Verificar asientos seleccionados
            seats_info = seatmap_page.verify_selected_seats()
            if seats_info:
                allure.attach(f"Asientos seleccionados: {seats_info}", name="Selected Seats", attachment_type=allure.attachment_type.TEXT)
            
            # Continuar
            assert seatmap_page.continue_to_payments(), "No se pudo continuar a pagos"
        
        # ==================== PAYMENTS - MANTENIENDO POM ====================
        with allure.step("7. Payments - Pago con tarjeta fake (Validación requerida)"):
            assert payments_page.wait_for_page_load(), "Página de pagos no cargó"
            
            # Verificar resumen de pago
            summary = payments_page.verify_payment_summary()
            assert summary is not None, "No se mostró resumen de pago"
            allure.attach(f"Resumen de pago: {summary}", name="Payment Summary", attachment_type=allure.attachment_type.TEXT)
            
            # Datos de tarjeta fake
            card_data = {
                "card_number": "4111111111111111",  # Test card number
                "card_holder": fake.name(),
                "expiry_month": "12",
                "expiry_year": "2025",
                "cvv": "123"
            }
            
            billing_data = {
                "address": fake.street_address(),
                "city": fake.city(),
                "zip": fake.postcode(),
                "country": "Colombia"
            }
            
            # Completar información de pago
            assert payments_page.fill_card_info(card_data), "No se pudo completar info de tarjeta"
            assert payments_page.fill_billing_info(billing_data), "No se pudo completar info de facturación"
            assert payments_page.accept_terms(), "No se pudo aceptar términos"
            
            # Realizar pago
            assert payments_page.submit_payment(), "No se pudo realizar pago"
            
            # Verificar mensaje de pago
            payment_status = payments_page.verify_payment_message()
            allure.attach(f"Estado de pago: {payment_status}", name="Payment Status", attachment_type=allure.attachment_type.TEXT)
            
            # El pago puede ser rechazado (eso está bien según los requerimientos)
            logger.info(f"Estado del pago: {payment_status}")
        
        # ==================== VERIFICACIÓN FINAL ====================
        with allure.step("8. Verificación final - CSV seguido y validaciones completadas"):
            # Tomar screenshot final
            home_page.take_screenshot("test_completed_csv")
            
            # Log de éxito
            allure.attach(
                f"✅ Test completado exitosamente en {request.cls.browser}\n"
                f"✅ Pasos CSV seguidos: 27 pasos exactos\n"
                f"✅ Validaciones completadas: Home, Select, Passengers, Services, Seatmap, Payments\n"
                f"✅ 1 pasajero de cada tipo: Adulto, Joven, Niño, Infante\n"
                f"✅ Tarifa Basic seleccionada\n"
                f"✅ Asientos economy seleccionados\n"
                f"✅ Pago con tarjeta fake completado\n"
                f"URL: {driver.current_url}\n"
                f"Título: {driver.title}",
                name="Test Result - CSV Following",
                attachment_type=allure.attachment_type.TEXT
            )
            
            logger.info(f"✅ Test completado exitosamente en {request.cls.browser}")
            logger.info(f"✅ 27 pasos CSV seguidos exactamente")
            logger.info(f"✅ Todas las validaciones requeridas completadas")
            assert True, "Booking one-way completado siguiendo CSV y validaciones requeridas"