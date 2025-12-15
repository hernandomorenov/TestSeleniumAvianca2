
# pages/passengers_page.py
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from utils.logger import logger


class PassengersPage(BasePage):
    """
    Página de información de pasajeros con modo TURBO basado en CSV (datos estáticos),
    usando JS click y esperas cortas para máxima velocidad y estabilidad.
    Incluye helpers para trabajar por 'anchor' (IDs dinámicos del CSV).
    """

    # ==================== Espera de carga ====================

    @allure.step("Passengers: esperar carga")
    def wait_for_page_load(self, timeout=12):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h1[contains(.,'Passengers') or contains(.,'Pasajeros')]|//booking-contact-custom")
                )
            )
            time.sleep(0.3)
            return True
        except Exception as e:
            logger.error(f"Passengers no cargó: {e}")
            return False

    # ==================== Helpers ultra-rápidos ====================

    def _js_click(self, el):
        self.driver.execute_script("arguments[0].scrollIntoView({behavior:'instant',block:'center'});", el)
        self.driver.execute_script("arguments[0].click();", el)

    def _click_by_id(self, _id, timeout=6):
        el = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.ID, _id)))
        self._js_click(el)
        return el

    def _type_by_id(self, _id, value, timeout=6):
        el = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.ID, _id)))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior:'instant',block:'center'});", el)
        el.clear()
        el.send_keys(value)
        time.sleep(0.3)  # Pequeña pausa para permitir visualización de entrada
        return el

    def _click_option_text(self, text, timeout=6):
        # Opción puede ser <button> o <span>, el CSV muestra ambos casos
        for locator in [(By.XPATH, f"//button[normalize-space()='{text}']"),
                        (By.XPATH, f"//span[normalize-space()='{text}']")]:
            try:
                opt = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
                self._js_click(opt)
                time.sleep(0.2)  # Pausa post-selección para renderizado
                return True
            except Exception:
                continue
        return False

    def _get_container_by_anchor(self, anchor, timeout=6):
        # Usamos IdFirstName<anchor> para encontrar el bloque local y scopear customerPrograms al pasajero correcto
        first_name = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.ID, f"IdFirstName{anchor}"))
        )
        container = first_name
        # Subir algunos niveles hasta un contenedor amplio del bloque de pasajero
        for _ in range(8):
            try:
                container = container.find_element(By.XPATH, "./..")
            except Exception:
                break
        return container

    def _click_customer_program_in_container(self, anchor):
        container = self._get_container_by_anchor(anchor)
        btns = container.find_elements(By.XPATH, ".//button[@id='customerPrograms']")
        if btns:
            self._js_click(btns[0])
            # Seleccionar "Not applicable"
            self._click_option_text("Not applicable")

    def _pick_birthdate_by_anchor(self, anchor, day, month_name, year):
        # Abre cada dropdown por ID y selecciona opción por texto (button/span)
        self._click_by_id(f"dateDayId_IdDateOfBirthHidden_{anchor}_")
        self._click_option_text(day)
        logger.info(f"  ✓ Día: {day}")
        time.sleep(0.3)

        self._click_by_id(f"dateMonthId_IdDateOfBirthHidden_{anchor}_")
        self._click_option_text(month_name)
        logger.info(f"  ✓ Mes: {month_name}")
        time.sleep(0.3)

        self._click_by_id(f"dateYearId_IdDateOfBirthHidden_{anchor}_")
        self._click_option_text(year)
        logger.info(f"  ✓ Año: {year}")
        time.sleep(0.3)

    # ==================== Llenado estático (idéntico al CSV) ====================

    @allure.step("Passengers (CSV estático): llenar todos rápido")
    def fill_passengers_static_from_csv(self):
        """
        Llena Adult (E32), Youth (E31), Child (E33), Infant (E34) y Contacto
        usando los mismos valores del CSV y clicks JS para máxima velocidad.
        """

        assert self.wait_for_page_load(), "❌ Passengers no cargó"

        # ---- Dataset estático exacto del CSV ----
        DATA = {
            "adult": {  # E32
                "anchor": "7E7E3533344234383244333232443435353835347E32",
                "gender": "Male",
                "first": "Hernando",
                "last":  "Moreno",
                "day":   "25",
                "month": "July",
                "year":  "1987",
                "nat":   "Colombia",
            },
            "youth": {  # E31
                "anchor": "7E7E3533344234383244333132443435353835347E31",
                "gender": "Female",
                "first": "Celeste",
                "last":  "Moreno",
                "day":   "24",
                "month": "April",
                "year":  "2025",
                "nat":   "Colombia",
            },
            "child": {  # E33
                "anchor": "7E7E3533344234383244333332443435353835347E33",
                "gender": "Male",
                "first": "Nicolas",
                "last":  "Moreno",
                "day":   "7",
                "month": "September",
                "year":  "2013",
                "nat":   "Colombia",
            },
            "infant": {  # E34
                "anchor": "7E7E3533344234383244333432443435353835347E34",
                "gender": "Male",
                "first": "Andres",
                "last":  "Moreno",
                "day":   "15",
                "month": "March",
                "year":  "2023",
                "nat":   "Colombia",
            },
            "contact": {
                "prefix": "Colombia",
                "phone":  "315542454521",
                "email":  "h@h.com",
                "confirm":"h@h.com",
                "newsletter": True
            }
        }

        # ---- 1) Adult (E32) ----
        logger.info("\n=== Llenando ADULTO ===")
        a = DATA["adult"]
        logger.info(f"  Género: {a['gender']}")
        self._click_by_id(f"IdPaxGender_{a['anchor']}")
        self._click_option_text(a["gender"])
        logger.info(f"  Nombre: {a['first']}")
        self._type_by_id(f"IdFirstName{a['anchor']}", a["first"])
        logger.info(f"  Apellido: {a['last']}")
        self._type_by_id(f"IdLastName{a['anchor']}", a["last"])
        logger.info(f"  Fecha: {a['day']}/{a['month']}/{a['year']}")
        self._pick_birthdate_by_anchor(a["anchor"], a["day"], a["month"], a["year"])
        logger.info(f"  Nacionalidad: {a['nat']}")
        self._click_by_id(f"IdDocNationality_{a['anchor']}"); self._click_option_text(a["nat"])
        logger.info("  Customer Program: Not applicable")
        self._click_customer_program_in_container(a["anchor"])
        time.sleep(0.5)
        logger.info("✅ ADULTO completado")
        self.take_screenshot("03_passengers_adult_completed")
        time.sleep(1.0)  # Pausa para validación visual

        # ---- 2) Youth (E31) ----
        logger.info("\n=== Llenando YOUTH ===")
        y = DATA["youth"]
        logger.info(f"  Género: {y['gender']}")
        self._click_by_id(f"IdPaxGender_{y['anchor']}"); self._click_option_text(y["gender"])
        logger.info(f"  Nombre: {y['first']}")
        self._type_by_id(f"IdFirstName{y['anchor']}", y["first"])
        logger.info(f"  Apellido: {y['last']}")
        self._type_by_id(f"IdLastName{y['anchor']}", y["last"])
        logger.info(f"  Fecha: {y['day']}/{y['month']}/{y['year']}")
        self._pick_birthdate_by_anchor(y["anchor"], y["day"], y["month"], y["year"])
        logger.info(f"  Nacionalidad: {y['nat']}")
        self._click_by_id(f"IdDocNationality_{y['anchor']}"); self._click_option_text(y["nat"])
        logger.info("  Customer Program: Not applicable")
        self._click_customer_program_in_container(y["anchor"])
        time.sleep(0.5)
        logger.info("✅ YOUTH completado")
        self.take_screenshot("03_passengers_youth_completed")
        time.sleep(1.0)  # Pausa para validación visual

        # ---- 3) Child (E33) ----
        logger.info("\n=== Llenando CHILD ===")
        c = DATA["child"]
        logger.info(f"  Género: {c['gender']}")
        self._click_by_id(f"IdPaxGender_{c['anchor']}"); self._click_option_text(c["gender"])
        logger.info(f"  Nombre: {c['first']}")
        self._type_by_id(f"IdFirstName{c['anchor']}", c["first"])
        logger.info(f"  Apellido: {c['last']}")
        self._type_by_id(f"IdLastName{c['anchor']}", c["last"])
        logger.info(f"  Fecha: {c['day']}/{c['month']}/{c['year']}")
        self._pick_birthdate_by_anchor(c["anchor"], c["day"], c["month"], c["year"])
        logger.info(f"  Nacionalidad: {c['nat']}")
        self._click_by_id(f"IdDocNationality_{c['anchor']}"); self._click_option_text(c["nat"])
        logger.info("  Customer Program: Not applicable")
        self._click_customer_program_in_container(c["anchor"])
        time.sleep(0.5)
        logger.info("✅ CHILD completado")
        self.take_screenshot("03_passengers_child_completed")
        time.sleep(1.0)  # Pausa para validación visual

        # ---- 4) Infant (E34) ----
        logger.info("\n=== Llenando INFANT ===")
        i = DATA["infant"]
        logger.info(f"  Género: {i['gender']}")
        self._click_by_id(f"IdPaxGender_{i['anchor']}"); self._click_option_text(i["gender"])
        logger.info(f"  Nombre: {i['first']}")
        self._type_by_id(f"IdFirstName{i['anchor']}", i["first"])
        logger.info(f"  Apellido: {i['last']}")
        self._type_by_id(f"IdLastName{i['anchor']}", i["last"])
        logger.info(f"  Fecha: {i['day']}/{i['month']}/{i['year']}")
        self._pick_birthdate_by_anchor(i["anchor"], i["day"], i["month"], i["year"])
        logger.info(f"  Nacionalidad: {i['nat']}")
        self._click_by_id(f"IdDocNationality_{i['anchor']}"); self._click_option_text(i["nat"])
        logger.info("  Customer Program: Not applicable")
        self._click_customer_program_in_container(i["anchor"])
        time.sleep(0.5)
        logger.info("✅ INFANT completado")
        self.take_screenshot("03_passengers_infant_completed")
        time.sleep(1.0)  # Pausa para validación visual

        # ---- 5) Contacto (global) ----
        logger.info("\n=== Llenando CONTACTO ===")
        logger.info(f"  Prefijo: {DATA['contact']['prefix']}")
        self._click_by_id("phone_prefixPhoneId"); self._click_option_text(DATA["contact"]["prefix"])
        time.sleep(0.3)
        logger.info(f"  Teléfono: {DATA['contact']['phone']}")
        self._type_by_id("phone_phoneNumberId", DATA["contact"]["phone"])
        logger.info(f"  Email: {DATA['contact']['email']}")
        self._type_by_id("email", DATA["contact"]["email"])
        logger.info(f"  Email Confirmación: {DATA['contact']['confirm']}")
        self._type_by_id("confirmEmail", DATA["contact"]["confirm"])

        if DATA["contact"]["newsletter"]:
            try:
                self._click_by_id("sendNewsLetter")
                logger.info("  Newsletter: ✓ marcado")
            except Exception:
                pass

        time.sleep(0.5)
        logger.info("✅ CONTACTO completado")
        self.take_screenshot("passengers_csv_static_filled")
        time.sleep(1.0)  # Pausa final antes de continuar
        return True

    # ==================== Continuar a Services ====================

    @allure.step("Passengers: continuar a Services")
    def continue_to_services(self):
        try:
            cont = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                    "//button[@class='button page_button btn-action page_button-primary-flow ng-star-inserted']//span[@class='button_label'][normalize-space()='Continue']"
                ))
            )
            self._js_click(cont)
            time.sleep(2.0)
            return True
        except Exception as e:
            logger.error(f"No se pudo continuar a Services: {e}")
            self.take_screenshot("continue_services_error")
