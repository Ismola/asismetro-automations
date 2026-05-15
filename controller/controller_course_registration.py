
import inspect
from actions.get_course_registration import get_course_registration
from actions.go_home import go_home
from actions.course_registration import course_registration
from actions.go_to_add_course_registration import go_to_add_course_registration
from actions.go_to_course_registration import go_to_course_registration
from actions.login import login
from actions.web_driver import close_driver, get_page
from utils.error import messageError
from datetime import datetime
from utils.file_manager import take_screenshot


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

        try:
            datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            raise messageError(
                "The field 'date' must have the format DD/MM/YYYY, e.g. '04/05/2026'")

    except KeyError as e:
        raise messageError(f"The field '{e.args[0]}' has not been sent")

    driver = None
    try:

        # You can choose betwen Chrome (default ) or firefox. Example: get_page('firefox')
        driver = get_page()

        # TODO: decominate to use login

        driver = login(driver, username, password)

        driver = go_home(driver)

        driver = go_to_course_registration(driver)

        driver = go_to_add_course_registration(driver)

        driver = course_registration(driver, data)

        driver = go_home(driver)

        driver = go_to_course_registration(driver)

        driver, course_registrations = get_course_registration(driver)

        return course_registrations

    except Exception as e:
        try:
            take_screenshot(driver)
        except:
            pass
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")

    finally:
        if driver is not None:
            close_driver(driver)
