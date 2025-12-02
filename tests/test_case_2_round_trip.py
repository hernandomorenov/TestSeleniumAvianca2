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
@allure.story("Round-trip Booking")
@pytest.mark.booking
@pytest.mark.regression
class TestCase2RoundTrip:
    """Caso 2: Booking Round-trip con diferentes tarifas y servicios"""
    
    @allure.title("Test 2: Round-trip booking with different fares - {browser}")
    @allure.description("Complete round-trip booking flow with Basic (ida) and Flex (vuelta) fares")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("booking", "round-trip", "multiple-fares")
    def test_round_trip_booking(self, driver, setup_test, request):
        # Inicializar páginas
        home_page = HomePage(driver)
        flight_page = FlightSelectionPage(driver)
        passengers_page = PassengersPage(driver)
        services_page = ServicesPage(driver)
        seatmap_page = SeatmapPage(driver)
        payments_page = PaymentsPage(driver)
        
        # ==================== HOME PAGE ====================
        with allure.step("1. Home Page - Configurar búsqueda round-trip"):
            # Navegar a la página
            assert home_page.navigate_to(setup_test), "No se pudo navegar a la página"
            
            # Seleccionar idioma
            assert home_page.select_language("english"), "No se pudo seleccionar idioma"
            
            # Seleccionar POS
            assert home_page.select_pos("spain"), "No se pudo seleccionar POS"
            
            # Configurar origen y destino
            assert home_page.set_origin_destination(
                Config.DEFAULT_ORIGIN, 
                Config.DEFAULT_DESTINATION
            ), "No se pudo configurar origen/destino"
            
            # Configurar pasajeros (1 de cada tipo)
            assert home_page.set_passengers(
                adults=1, 
                youth=1, 
                children=1, 
                infants=1
            ), "No se pudo configurar pasajeros"
            
            # Seleccionar tipo de viaje round-trip
            assert home_page.select_trip_type("round-trip"), "No se pudo seleccionar round-trip"
            
            # Buscar vuelos
            assert home_page.search_flights(), "No se pudo buscar vuelos"
        
        # ==================== SELECT FLIGHT ====================
        with allure.step("2. Select Flight - Seleccionar tarifas Basic (ida) y Flex (vuelta)"):
            assert flight_page.wait_for_page_load(), "Página de vuelos no cargó"
            
            # Seleccionar tarifa Basic para ida
            assert flight_page.select_fare_type("basic"), "No se pudo seleccionar tarifa Basic"
            
            # Seleccionar vuelo de ida
            assert flight_page.select_departure_flight(), "No se pudo seleccionar vuelo de ida"
            
            # Seleccionar tarifa Flex para vuelta
            assert flight_page.select_fare_type("flex"), "No se pudo seleccionar tarifa Flex"
            
            # Seleccionar vuelo de vuelta
            assert flight_page.select_return_flight(), "No se pudo seleccionar vuelo de vuelta"
            
            # Verificar precios
            price = flight_page.verify_flight_price()
            if price:
                allure.attach(f"Precio total: {price}", name="Total Price", attachment_type=allure.attachment_type.TEXT)
            
            # Continuar
            assert flight_page.continue_to_passengers(), "No se pudo continuar a pasajeros"
        
        # ==================== PASSENGERS ====================
        with allure.step("3. Passengers - Ingresar información"):
            assert passengers_page.wait_for_page_load(), "Página de pasajeros no cargó"
            
            # Preparar datos fake
            passenger_data = {
                "adult": {
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "gender": "Female",
                    "document": str(fake.random_number(digits=10))
                },
                "youth": {
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name()
                },
                "child": {
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name()
                },
                "infant": {
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name()
                },
                "contact": {
                    "email": fake.email(),
                    "phone": fake.phone_number()[:15]
                }
            }
            
            # Completar información
            assert passengers_page.fill_all_passengers_info(passenger_data), \
                "No se pudo completar información de pasajeros"
            
            # Continuar
            assert passengers_page.continue_to_services(), "No se pudo continuar a servicios"
        
        # ==================== SERVICES ====================
        with allure.step("4. Services - Seleccionar Avianca Lounges o cualquier servicio"):
            assert services_page.wait_for_page_load(), "Página de servicios no cargó"
            
            # Intentar seleccionar Avianca Lounge
            lounge_selected = services_page.select_avianca_lounge()
            
            # Si no está disponible, seleccionar cualquier servicio
            if not lounge_selected:
                assert services_page.select_any_service(), "No se pudo seleccionar ningún servicio"
            
            # Continuar
            assert services_page.continue_to_seatmap(), "No se pudo continuar a asientos"
        
        # ==================== SEATMAP ====================
        with allure.step("5. Seatmap - Seleccionar diferentes tipos de asientos"):
            assert seatmap_page.wait_for_page_load(), "Página de asientos no cargó"
            
            # Intentar seleccionar diferentes tipos de asientos
            seat_types = ["plus", "economy", "premium", "economy"]
            seatmap_page.select_multiple_seat_types(seat_types)
            
            # Verificar asientos
            seats_info = seatmap_page.verify_selected_seats()
            if seats_info:
                allure.attach(f"Asientos seleccionados: {seats_info}", name="Selected Seats", attachment_type=allure.attachment_type.TEXT)
            
            # Continuar
            assert seatmap_page.continue_to_payments(), "No se pudo continuar a pagos"
        
        # ==================== PAYMENTS ====================
        with allure.step("6. Payments - Llenar información pero no enviar"):
            assert payments_page.wait_for_page_load(), "Página de pagos no cargó"
            
            # Verificar resumen
            summary = payments_page.verify_payment_summary()
            assert summary is not None, "No se mostró resumen de pago"
            
            # Datos de tarjeta fake
            card_data = {
                "card_number": "5555555555554444",  # MasterCard test number
                "card_holder": fake.name(),
                "expiry_month": "06",
                "expiry_year": "2026",
                "cvv": "456"
            }
            
            billing_data = {
                "address": fake.street_address(),
                "city": fake.city(),
                "zip": fake.postcode(),
                "country": "Spain"
            }
            
            # Completar información PERO NO ENVIAR
            assert payments_page.fill_payment_but_not_submit(card_data, billing_data), \
                "No se pudo completar información de pago"
            
            # Verificar que el botón de pago está disponible pero NO hacer click
            pay_button = payments_page.wait_for_element(payments_page.PAY_NOW_BUTTON, "Botón pagar")
            assert pay_button and pay_button.is_enabled(), "Botón de pago no está habilitado"
            
            # NO hacer click en "Pagar ahora" (requerimiento del test)
            allure.attach(
                "Información de pago completada pero NO enviada (como se solicita en los requerimientos)",
                name="Payment Info Status",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # ==================== VERIFICACIÓN FINAL ====================
        with allure.step("7. Verificación final - Test completado"):
            # Tomar screenshot final
            home_page.take_screenshot("round_trip_completed")
            
            allure.attach(
                f"Round-trip booking test completado exitosamente en {request.cls.browser}\n"
                f"URL final: {driver.current_url}\n"
                f"Información de pago completada pero no enviada",
                name="Test Result",
                attachment_type=allure.attachment_type.TEXT
            )
            
            logger.info(f"✅ Round-trip test completado en {request.cls.browser}")
            assert True, "Round-trip booking completado exitosamente"