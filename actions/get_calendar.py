import inspect
import logging
import os
from selenium_scraper_runtime.elements import click_element
from selenium_scraper_runtime.elements import search_element
from utils.config import DOWNLOAD_DIR, DOWNLOAD_MAX_TIMEOUT
from utils.error import messageError
from utils.file_manager import (
    create_download_directory,
    delete_file,
    read_and_delete_download,
)
from selenium.webdriver.common.by import By


def get_calendar(driver, optional=False):
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    try:
        download_directory = create_download_directory(DOWNLOAD_DIR)
        calendar_filename = "CalendarioAsismetro.ics"
        calendar_path = os.path.join(download_directory, calendar_filename)
        delete_file(calendar_path)
        delete_file(f"{calendar_path}.crdownload")
        delete_file(f"{calendar_path}.part")

        agenda_button = search_element(driver, (
            By.XPATH,
            '//button[@type="button" and contains(concat(" ", normalize-space(@class), " "), " calendar-header-action ") and @onclick="cambio(\'10\',\'\',\'\',\'\')"]'
        ), raise_exception=not optional)
        if agenda_button is None:
            logging.info("Calendar export is not available")
            return driver, None

        driver = click_element(driver, agenda_button)
        try:
            calendar = read_and_delete_download(
                download_directory,
                calendar_filename,
                timeout=DOWNLOAD_MAX_TIMEOUT,
            )
        except messageError as error:
            if not optional:
                raise
            logging.warning("Optional calendar download is unavailable: %s", error)
            delete_file(calendar_path)
            delete_file(f"{calendar_path}.crdownload")
            delete_file(f"{calendar_path}.part")
            return driver, None

        return driver, calendar
    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
