
import inspect
from actions.get_calendar import get_calendar
from actions.go_home import go_home
from actions.go_to_actual_calendar import go_to_actual_calendar
from actions.go_to_calendars import go_to_calendars
from actions.go_to_next_calendar import go_to_next_calendar
from actions.login import login
from actions.web_driver import close_driver, get_page
from utils.error import messageError
from utils.file_manager import take_screenshot

def controller_get_calendar(data):

    try:
        username = data['username']
        password = data['password']

    except KeyError as e:
        raise messageError(f"The field '{e.args[0]}' has not been sent")

    driver = None
    try:

        # You can choose betwen Chrome (default ) or firefox. Example: get_page('firefox')
        driver = get_page()

        # TODO: decominate to use login

        driver = login(driver, username, password)

        driver = go_home(driver)

        driver = go_to_calendars(driver)

        driver = go_to_actual_calendar(driver)
        
        driver, actual_calendar = get_calendar(driver)

        driver = go_home(driver)

        driver = go_to_calendars(driver)

        driver = go_to_next_calendar(driver)

        driver, next_calendar = get_calendar(driver)

        return {
            "actual_calendar": actual_calendar,
            "next_calendar": next_calendar
        }

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
