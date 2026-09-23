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
