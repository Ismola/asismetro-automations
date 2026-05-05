import inspect
import logging
from time import sleep
from actions.click_element import click_element
from actions.search_element import search_element
from utils.error import messageError
from selenium.webdriver.common.by import By


def go_to_next_calendar(driver):
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    try:

        course_registration_link = search_element(driver, (
            By.XPATH, '//input[@name="mes" and @value="Mes Siguiente" and @type="submit"]'
        ))
        driver = click_element(driver, course_registration_link)
        
        sleep(1)

        return driver
    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
