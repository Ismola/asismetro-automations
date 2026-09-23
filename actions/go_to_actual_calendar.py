import inspect
import logging
from time import sleep
from selenium_scraper_runtime.elements import click_element
from selenium_scraper_runtime.elements import search_element
from utils.error import messageError
from selenium.webdriver.common.by import By



def go_to_actual_calendar(driver):
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    try:

        course_registration_link = search_element(driver, (
            By.XPATH, '//input[@name="mes" and @value="Mes Actual" and @type="submit"]'
        ))
        driver = click_element(driver, course_registration_link)
        
        sleep(1)

        return driver
    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
