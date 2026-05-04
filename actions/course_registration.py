import inspect
import logging
from actions.click_element import click_element
from actions.search_element import search_element
from actions.write_element import write_element
from utils.config import STAGE
from utils.error import messageError
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def course_registration(driver, data):
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    try:

        # DATE
        day, month, year = data["date"].split("/")

        day_select = search_element(driver, (
            By.XPATH, '//select[@name="FechaRegistroDay"]'
        ))
        Select(day_select).select_by_value(str(int(day)))

        month_select = search_element(driver, (
            By.XPATH, '//select[@name="FechaRegistroMonth"]'
        ))
        Select(month_select).select_by_value(str(int(month)))

        year_select = search_element(driver, (
            By.XPATH, '//select[@name="FechaRegistroYear"]'
        ))
        Select(year_select).select_by_value(year)

        # SHIFT

        shift_radio = search_element(driver, (
            By.XPATH, f'//input[@type="radio"][@name="IdTurno"][@value="{data["shift"]}"]'
        ), wait_to_search=False)
        driver.execute_script("arguments[0].click();", shift_radio)

        # Activity

        activity_radio = search_element(driver, (
            By.XPATH, f'//label[normalize-space(text())="{data["activity"]}"]/preceding-sibling::input[@name="IdPublicacion"]'
        ), wait_to_search=False)
        driver.execute_script("arguments[0].click();", activity_radio)

        # Number

        number_input = search_element(driver, (
            By.XPATH, '//input[@name="CantidadColocada"][@id="CantidadColocada"]'
        ))
        driver = write_element(driver, number_input, data["number"])

        # Guardar
        save_button = search_element(driver, (
            By.XPATH, '//button[@id="insert"][@name="insert_x"][@type="submit"]'
        ))
        if STAGE != "staging":
            driver = click_element(driver, save_button)
        else:
            logging.info("STAGE is staging, skipping click on save button")

        return driver
    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
