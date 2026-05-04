import inspect
import logging
from actions.click_element import click_element
from actions.search_element import search_element
from utils.config import STAGE
from utils.error import messageError
from selenium.webdriver.common.by import By


def go_to_course_registration(driver):
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    try:
        course_registration_link = search_element(driver, (
            By.XPATH, '//a[@href="t_registros_publicaciones_ppam_publicador_view.php"]'
        ))
        driver = click_element(driver, course_registration_link)

        add_button = search_element(driver, (
            By.XPATH, '//button[@id="addNew" and @name="addNew_x" and @type="submit"]'
        ))
        driver = click_element(driver, add_button)

        return driver
    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
