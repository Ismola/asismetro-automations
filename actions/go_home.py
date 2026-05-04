import inspect
import logging
from actions.click_element import click_element
from actions.search_element import search_element
from utils.error import messageError
from selenium.webdriver.common.by import By


def go_home(driver):
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    try:
        home_link = search_element(driver, (
            By.XPATH, '//a[@class="navbar-brand"][@href="index.php"]'
        ))
        driver = click_element(driver, home_link)

        return driver
    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
