import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    comfort_tariff = (
        By.XPATH,
        "//div[contains(@class, 'tcard')][.//div[@class='tcard-title' and text()='Comfort']]"
    )

    request_taxi_button = (
        By.XPATH,
        "//button[text()='Pedir un taxi']"
    )

    phone_button = (By.CLASS_NAME, 'np-button')

    phone_field = (By.ID, 'phone')

    phone_next_button = (
        By.XPATH,
        "//button[@type='submit' and text()='Siguiente']"
    )

    phone_code_field = (By.ID, 'code')

    phone_confirm_button = (
        By.XPATH,
        "//button[@type='submit' and text()='Confirmar']"
    )

    payment_method_button = (
        By.XPATH,
        "//div[contains(@class, 'pp-button')][.//div[@class='pp-text' and text()='Método de pago']]"
    )

    add_card_option = (
        By.XPATH,
        "//div[contains(@class, 'pp-row')][.//div[@class='pp-title' and text()='Agregar tarjeta']]"
    )

    card_number_field = (By.ID, 'number')

    card_code_field = (By.CSS_SELECTOR, 'input.card-input#code')

    card_add_button = (
        By.XPATH,
        "//button[@type='submit' and text()='Agregar']"
    )

    payment_modal_close_button = (
        By.CSS_SELECTOR,
        '.payment-picker .section-close'
    )

    driver_message_field = (By.ID, 'comment')

    blanket_switch = (
        By.XPATH,
        "//div[contains(@class, 'r-sw-container')][.//div[@class='r-sw-label' and normalize-space()='Manta y pañuelos']]//div[@class='switch']"
    )

    blanket_checkbox = (
        By.XPATH,
        "//div[contains(@class, 'r-sw-container')][.//div[@class='r-sw-label' and normalize-space()='Manta y pañuelos']]//input[@type='checkbox']"
    )

    ice_cream_plus_button = (
        By.XPATH,
        "//div[contains(@class, 'r-counter-container')][.//div[@class='r-counter-label' and normalize-space()='Helado']]//div[contains(@class, 'counter-plus')]"
    )

    ice_cream_counter = (
        By.XPATH,
        "//div[contains(@class, 'r-counter-container')][.//div[@class='r-counter-label' and normalize-space()='Helado']]//div[@class='counter-value']"
    )

    booking_button = (By.CLASS_NAME, 'smart-button')

    search_car_modal = (
        By.XPATH,
        "//div[contains(@class, 'order') and contains(@class, 'shown')]"
        "[.//div[contains(@class, 'order-header') and contains(., 'Buscar automóvil')]]"
    )

    def __init__(self, driver):
        self.driver = driver

    def wait_for_load_page(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                self.from_field
            )
        )

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def select_comfort_tariff(self):
        self.driver.find_element(*self.comfort_tariff).click()

    def is_comfort_tariff_selected(self):
        comfort_card = self.driver.find_element(*self.comfort_tariff)
        return "active" in comfort_card.get_attribute("class").split()

    def click_request_taxi_button(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.request_taxi_button
            )
        ).click()

    def click_phone_button(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.phone_button
            )
        ).click()

    def set_phone(self, phone_number):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                self.phone_field
            )
        ).send_keys(phone_number)

    def click_phone_next_button(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.phone_next_button
            )
        ).click()

    def set_phone_code(self, code):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                self.phone_code_field
            )
        ).send_keys(code)

    def click_phone_confirm_button(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.phone_confirm_button
            )
        ).click()

    def enter_phone_number(self, phone_number):
        self.click_phone_button()
        self.set_phone(phone_number)
        self.click_phone_next_button()

    def wait_for_phone_confirmation(self):
        return WebDriverWait(self.driver, 10).until(
            expected_conditions.invisibility_of_element_located(
                self.phone_code_field
            )
        )

    def click_payment_method_button(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.payment_method_button
            )
        ).click()

    def click_add_card_option(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.add_card_option
            )
        ).click()

    def set_card_number(self, card_number):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                self.card_number_field
            )
        ).send_keys(card_number)

    def set_card_code(self, card_code):
        code_field = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                self.card_code_field
            )
        )
        code_field.send_keys(card_code)
        code_field.send_keys(Keys.TAB)

    def click_card_add_button(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.card_add_button
            )
        ).click()

    def close_payment_modal(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.payment_modal_close_button
            )
        ).click()

    def add_card(self, card_number, card_code):
        self.click_payment_method_button()
        self.click_add_card_option()
        self.set_card_number(card_number)
        self.set_card_code(card_code)
        self.click_card_add_button()
        self.close_payment_modal()

    def wait_for_card_form_to_close(self):
        return WebDriverWait(self.driver, 10).until(
            expected_conditions.invisibility_of_element_located(
                self.card_add_button
            )
        )

    def set_driver_message(self, message):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                self.driver_message_field
            )
        ).send_keys(message)

    def get_driver_message(self):
        return self.driver.find_element(
            *self.driver_message_field
        ).get_property('value')

    def enable_blanket_and_tissues(self):
        # Comprobar el estado actual
        if not self.is_blanket_and_tissues_enabled():
            WebDriverWait(self.driver, 10).until(
                expected_conditions.element_to_be_clickable(
                    self.blanket_switch
                )
            ).click()

        # Verificar que la opción quede activada
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.is_blanket_and_tissues_enabled()
        )

    def is_blanket_and_tissues_enabled(self):
        return self.driver.find_element(
            *self.blanket_checkbox
        ).is_selected()

    def add_ice_cream(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.ice_cream_plus_button
            )
        ).click()

    def get_ice_cream_count(self):
        return int(
            self.driver.find_element(
                *self.ice_cream_counter
            ).text
        )

    def click_booking_button(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.booking_button
            )
        ).click()

    def is_search_car_modal_visible(self):
        return WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                self.search_car_modal
            )
        ).is_displayed()

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')



class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # Corrección de compatibilidad: la plantilla original de TripleTen utiliza
        # desired_capabilities, argumento no admitido por Selenium 4.52.0.
        # Se reemplaza por ChromeOptions() y set_capability(), conservando
        # el registro de rendimiento necesario para retrieve_phone_code().
        options = webdriver.ChromeOptions()
        options.set_capability(
            "goog:loggingPrefs",
            {"performance": "ALL"}
        )

        # Crear el controlador Chrome
        cls.driver = webdriver.Chrome(options=options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_load_page()
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_tariff(self):
        self.driver.get(data.urban_routes_url)

        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_load_page()

        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_request_taxi_button()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                routes_page.comfort_tariff
            )
        )

        routes_page.select_comfort_tariff()

        assert routes_page.is_comfort_tariff_selected()

    def test_phone_number(self):
        # Abrir Urban Routes
        self.driver.get(data.urban_routes_url)

        # Crear el objeto de página
        routes_page = UrbanRoutesPage(self.driver)

        # Esperar a que cargue la página
        routes_page.wait_for_load_page()

        # Configurar las direcciones
        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        # Abrir el panel de tarifas
        routes_page.click_request_taxi_button()

        # Esperar a que Comfort esté disponible
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                routes_page.comfort_tariff
            )
        )

        # Seleccionar Comfort
        routes_page.select_comfort_tariff()

        # Introducir el número y solicitar el código SMS
        routes_page.enter_phone_number(data.phone_number)

        # Esperar a que aparezca el formulario de confirmación SMS
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                routes_page.phone_code_field
            )
        )

        # Obtener el código de confirmación con la función oficial
        code = retrieve_phone_code(self.driver)

        # Introducir el código
        routes_page.set_phone_code(code)

        # Confirmar el código
        routes_page.click_phone_confirm_button()

        # Comprobar que desaparece el formulario SMS
        assert routes_page.wait_for_phone_confirmation(), \
            "El formulario de confirmación SMS no se cerró"

    def test_add_card(self):
        # Abrir Urban Routes
        self.driver.get(data.urban_routes_url)

        # Crear el objeto de página y esperar su carga
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_load_page()

        # Configurar las direcciones
        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        # Abrir las tarifas y seleccionar Comfort
        routes_page.click_request_taxi_button()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                routes_page.comfort_tariff
            )
        )

        routes_page.select_comfort_tariff()

        # Agregar la tarjeta con los datos de prueba
        routes_page.add_card(
            data.card_number,
            data.card_code
        )

        # Comprobar que se cerró el formulario de tarjeta
        assert routes_page.wait_for_card_form_to_close(), \
            "El formulario para agregar la tarjeta no se cerró"

    def test_driver_message(self):
        # Abrir Urban Routes
        self.driver.get(data.urban_routes_url)

        # Crear el objeto POM y esperar la carga
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_load_page()

        # Configurar origen y destino
        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        # Abrir el panel de tarifas
        routes_page.click_request_taxi_button()

        # Esperar a que Comfort esté disponible
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                routes_page.comfort_tariff
            )
        )

        # Seleccionar Comfort
        routes_page.select_comfort_tariff()

        # Introducir el mensaje para el conductor
        routes_page.set_driver_message(data.message_for_driver)

        # Comprobar que el mensaje coincide con el esperado
        assert routes_page.get_driver_message() == data.message_for_driver, \
            "El mensaje para el conductor no coincide con el esperado"

    def test_blanket_and_tissues(self):
        # Abrir Urban Routes
        self.driver.get(data.urban_routes_url)

        # Crear el objeto POM y esperar la carga
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_load_page()

        # Configurar las direcciones
        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        # Abrir el panel de tarifas
        routes_page.click_request_taxi_button()

        # Esperar a que Comfort esté disponible
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                routes_page.comfort_tariff
            )
        )

        # Seleccionar la tarifa Comfort
        routes_page.select_comfort_tariff()

        # Activar manta y pañuelos
        routes_page.enable_blanket_and_tissues()

        # Comprobar que el interruptor está activado
        assert routes_page.is_blanket_and_tissues_enabled(), \
            "La opción Manta y pañuelos no quedó activada"

    def test_two_ice_creams(self):
        # Abrir Urban Routes
        self.driver.get(data.urban_routes_url)

        # Crear el objeto POM y esperar la carga
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_load_page()

        # Configurar origen y destino
        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        # Abrir el panel de tarifas
        routes_page.click_request_taxi_button()

        # Esperar a que Comfort esté disponible
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                routes_page.comfort_tariff
            )
        )

        # Seleccionar Comfort
        routes_page.select_comfort_tariff()

        # Solicitar dos helados
        routes_page.add_ice_cream()
        routes_page.add_ice_cream()

        # Comprobar que la cantidad sea exactamente 2
        assert routes_page.get_ice_cream_count() == 2, \
            "La cantidad de helados no es igual a 2"

    def test_book_taxi(self):
        # Abrir Urban Routes y esperar la carga
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_load_page()

        # Configurar origen y destino
        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        # Abrir tarifas y seleccionar Comfort
        routes_page.click_request_taxi_button()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                routes_page.comfort_tariff
            )
        )

        routes_page.select_comfort_tariff()

        # Introducir y confirmar el teléfono
        routes_page.enter_phone_number(data.phone_number)

        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                routes_page.phone_code_field
            )
        )

        code = retrieve_phone_code(self.driver)
        routes_page.set_phone_code(code)
        routes_page.click_phone_confirm_button()

        assert routes_page.wait_for_phone_confirmation(), \
            "El teléfono no se confirmó correctamente"

        # Agregar la tarjeta
        routes_page.add_card(
            data.card_number,
            data.card_code
        )

        assert routes_page.wait_for_card_form_to_close(), \
            "El formulario de tarjeta no se cerró"

        # Escribir el mensaje para el conductor
        routes_page.set_driver_message(data.message_for_driver)

        # Activar manta y pañuelos
        routes_page.enable_blanket_and_tissues()

        # Solicitar dos helados
        routes_page.add_ice_cream()
        routes_page.add_ice_cream()

        # Comprobar los requisitos del pedido
        assert routes_page.is_comfort_tariff_selected()
        assert routes_page.get_driver_message() == data.message_for_driver
        assert routes_page.is_blanket_and_tissues_enabled()
        assert routes_page.get_ice_cream_count() == 2

        # Solicitar el taxi
        routes_page.click_booking_button()

        # Verificar que aparece el modal de búsqueda
        assert routes_page.is_search_car_modal_visible(), \
            "No apareció el modal Buscar automóvil"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
