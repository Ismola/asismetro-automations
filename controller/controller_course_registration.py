
import inspect
import logging
from actions.go_to_course_registration import go_to_course_registration
from actions.login import login
from actions.web_driver import close_driver, get_page
from utils.error import messageError

# NO BORRAR PARA QUE LOS TEST DE LA PIPELINE NO DEN ERROR


def controller_course_registration(data):

    try:
        username = data['username']
        password = data['password']
        date = data["date"]
        shift = data["shift"]
        activity = data["activity"]
        number = data["number"]

        valid_activities = ["Curso Bíblico Iniciado",
                            "Sin Cursos Bíblicos", "Turno Anulado"]
        if activity not in valid_activities:
            raise messageError(
                f"The field 'activity' must be one of: {', '.join(valid_activities)}")

        valid_shifts = ["1", "2", "3", "4"]
        if shift not in valid_shifts:
            raise messageError(
                f"The field 'shift' must be one of: {', '.join(valid_shifts)}")

    except KeyError as e:
        raise messageError(f"The field '{e.args[0]}' has not been sent")

    driver = None
    try:
        message = "ok"

        # You can choose betwen Chrome (default ) or firefox. Example: get_page('firefox')
        driver = get_page()

        # TODO: decominate to use login

        driver = login(driver, username, password)

        driver = go_to_course_registration(driver)

        # Add actions

        return message

    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")

    finally:
        if driver is not None:
            close_driver(driver)
