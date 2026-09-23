import inspect
import logging
from selenium_scraper_runtime.elements import click_element
from selenium_scraper_runtime.elements import search_element
from utils.error import messageError
from selenium.webdriver.common.by import By


def go_to_calendars(driver):
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    try:

        calendar_link = search_element(driver, (
            By.XPATH, '//a[@href="verCalendarioTurnosView.php"]'
        ))
        driver = click_element(driver, calendar_link)

        return driver
    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
