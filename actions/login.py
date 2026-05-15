import inspect
from time import sleep
from actions.click_element import click_element
from actions.search_element import search_element
from actions.write_element import write_element
from utils.error import messageError
from selenium.webdriver.common.by import By
import logging

# The driver must have accessed the target url


def login(driver, username, password):
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    try:
        user_input = search_element(driver, (
            By.CSS_SELECTOR, 'input[placeholder="Email Usuario"]'
        ))
        driver = write_element(driver, user_input, username)

        password_input = search_element(driver, (
            By.CSS_SELECTOR, 'input[type="password"][placeholder="Clave"]'
        ))
        driver = write_element(driver, password_input, password)

        button_input = search_element(driver, (
            By.CSS_SELECTOR, 'button[name="signIn"][type="submit"][id="submit"]'
        ))
        driver = click_element(driver, button_input)

        sleep(2)

        return driver
    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
