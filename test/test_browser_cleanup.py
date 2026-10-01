from unittest.mock import Mock

import pytest

from controller import controller_course_registration, controller_get_calendar, controller_sample
from utils.error import messageError


def test_sample_closes_driver_after_success(monkeypatch):
    driver = Mock()
    close = Mock()
    monkeypatch.setattr(controller_sample, "get_page", Mock(return_value=driver))
    monkeypatch.setattr(controller_sample, "close_driver", close)

    assert controller_sample.controller_sample({"username": "u", "password": "p"}) == "ok"
    close.assert_called_once_with(driver)


def test_calendar_closes_driver_when_site_action_fails(monkeypatch):
    driver = Mock()
    close = Mock()
    monkeypatch.setattr(controller_get_calendar, "get_page", Mock(return_value=driver))
    monkeypatch.setattr(controller_get_calendar, "login", Mock(side_effect=RuntimeError("site failure")))
    monkeypatch.setattr(controller_get_calendar, "close_driver", close)
    monkeypatch.setattr(controller_get_calendar, "take_screenshot", Mock())

    with pytest.raises(messageError):
        controller_get_calendar.controller_get_calendar({"username": "u", "password": "p"})

    close.assert_called_once_with(driver)


@pytest.mark.parametrize("next_month_available", [False, True])
def test_calendar_returns_current_month_when_next_month_is_missing(monkeypatch, next_month_available):
    driver = Mock()
    actual_calendar = {"name": "Turnos", "timezone": "Europe/Madrid", "events": []}
    close = Mock()
    monkeypatch.setattr(controller_get_calendar, "get_page", Mock(return_value=driver))
    monkeypatch.setattr(controller_get_calendar, "login", Mock(return_value=driver))
    monkeypatch.setattr(controller_get_calendar, "go_to_actual_calendar", Mock(return_value=driver))
    monkeypatch.setattr(
        controller_get_calendar,
        "get_calendar",
        Mock(side_effect=[(driver, actual_calendar), (driver, None)]),
    )
    monkeypatch.setattr(driver, "back", Mock())
    monkeypatch.setattr(
        controller_get_calendar,
        "go_to_next_calendar",
        Mock(return_value=(driver, next_month_available)),
    )
    monkeypatch.setattr(controller_get_calendar, "close_driver", close)
    monkeypatch.setattr(controller_get_calendar, "take_screenshot", Mock())

    result = controller_get_calendar.controller_get_calendar({"username": "u", "password": "p"})

    assert result == {"actual_calendar": actual_calendar, "next_calendar": None}
    close.assert_called_once_with(driver)


def test_registration_closes_driver_when_site_action_fails(monkeypatch):
    driver = Mock()
    close = Mock()
    monkeypatch.setattr(controller_course_registration, "get_page", Mock(return_value=driver))
    monkeypatch.setattr(controller_course_registration, "login", Mock(side_effect=RuntimeError("site failure")))
    monkeypatch.setattr(controller_course_registration, "close_driver", close)
    monkeypatch.setattr(controller_course_registration, "take_screenshot", Mock())

    data = {
        "username": "u",
        "password": "p",
        "date": "04/05/2026",
        "shift": "1",
        "activity": "Curso Bíblico Iniciado",
        "number": "1",
    }
    with pytest.raises(messageError):
        controller_course_registration.controller_course_registration(data)

    close.assert_called_once_with(driver)
