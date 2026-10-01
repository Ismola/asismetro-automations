import inspect
import logging
import os

from selenium.webdriver.common.by import By
from selenium_scraper_runtime.elements import click_element, search_element

from utils.config import DOWNLOAD_DIR, DOWNLOAD_MAX_TIMEOUT
from utils.calendar import calendar_to_json, parse_calendar_export
from utils.error import messageError
from utils.file_manager import (
    create_download_directory,
    delete_file,
    read_and_delete_download,
)


def get_calendar(driver, optional=False):
    """Download the iCalendar export and return its events as JSON data.

    AsisMetro keeps the user on the calendar page when exporting, so the
    export is read from the browser's download directory instead of the page.
    A missing Agenda button or export is allowed for the optional next month.
    """
    logging.info("START || %s", inspect.currentframe().f_code.co_name)
    try:
        download_directory = create_download_directory(DOWNLOAD_DIR)
        calendar_filename = "CalendarioAsismetro.ics"
        calendar_path = os.path.join(download_directory, calendar_filename)
        partial_paths = (f"{calendar_path}.crdownload", f"{calendar_path}.part")

        # Remove a previous export so it cannot be mistaken for this month's
        # download if AsisMetro does not start a new one.
        delete_file(calendar_path)
        for partial_path in partial_paths:
            delete_file(partial_path)

        agenda_button = search_element(
            driver,
            (
                By.XPATH,
                '//button[@type="button" and '
                '(contains(concat(" ", normalize-space(@class), " "), " calendar-header-action ") '
                'or contains(translate(normalize-space(.), "agenda", "AGENDA"), "AGENDA") '
                'or @aria-label="Agenda" or @title="Agenda")]'
            ),
            raise_exception=not optional,
        )
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
            calendar = calendar_to_json(parse_calendar_export(calendar))
        except messageError as error:
            if not optional:
                raise
            logging.info("Optional next-month calendar export is unavailable: %s", error)
            for partial_path in partial_paths:
                delete_file(partial_path)
            delete_file(calendar_path)
            return driver, None

        return driver, calendar
    except Exception as error:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {error}"
        ) from error
