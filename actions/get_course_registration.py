import inspect
import logging
from utils.error import messageError
from selenium.webdriver.common.by import By


def get_course_registration(driver):
    logging.info(f"START || {inspect.currentframe().f_code.co_name}")
    try:
        course_registrations = []

        rows = driver.find_elements(
            By.XPATH,
            '//table[@data-tablename="t_registros_publicaciones_ppam_publicador"]/tbody/tr[@data-id]'
        )

        for row in rows:
            record_id = row.get_attribute("data-id")
            date = row.find_element(
                By.XPATH, f'.//td[contains(@id, "FechaRegistro-{record_id}")]').text.strip()
            ppam = row.find_element(
                By.XPATH, f'.//td[contains(@id, "IdPPAM-{record_id}")]').text.strip()
            shift = row.find_element(
                By.XPATH, f'.//td[contains(@id, "IdTurno-{record_id}")]').text.strip()
            activity = row.find_element(
                By.XPATH, f'.//td[contains(@id, "IdPublicacion-{record_id}")]').text.strip()
            quantity = row.find_element(
                By.XPATH, f'.//td[contains(@id, "CantidadColocada-{record_id}")]').text.strip()

            course_registrations.append({
                "id": record_id,
                "date": date,
                "ppam": ppam,
                "shift": shift,
                "activity": activity,
                "quantity": quantity,
            })

        return driver, course_registrations
    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")
