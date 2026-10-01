from pathlib import Path
from unittest.mock import Mock

import pytest

from actions import get_calendar as calendar_action
from utils.error import messageError


def test_get_calendar_returns_downloaded_ics(tmp_path, monkeypatch):
    driver = Mock()
    agenda_button = object()
    ics_content = (
        "BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Calendar test//ES\r\n"
        "BEGIN:VEVENT\r\nUID:test-shift\r\nDTSTART:20261010T090000Z\r\n"
        "DTEND:20261010T120000Z\r\nSUMMARY:Turno\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n"
    )
    monkeypatch.setattr(calendar_action, "DOWNLOAD_DIR", str(tmp_path))
    monkeypatch.setattr(calendar_action, "search_element", Mock(return_value=agenda_button))

    def click_and_create_download(current_driver, button):
        assert current_driver is driver
        assert button is agenda_button
        export = "<style>.home { color: blue; }</style>\n<div>Inicio</div>\n" + ics_content
        (Path(tmp_path) / "CalendarioAsismetro.ics").write_text(export, encoding="utf-8")
        return current_driver

    monkeypatch.setattr(calendar_action, "click_element", click_and_create_download)

    returned_driver, calendar = calendar_action.get_calendar(driver)

    assert returned_driver is driver
    assert calendar == {
        "name": None,
        "timezone": None,
        "events": [{
            "uid": "test-shift",
            "summary": "Turno",
            "description": None,
            "location": None,
            "start": "2026-10-10T09:00:00+00:00",
            "end": "2026-10-10T12:00:00+00:00",
            "all_day": False,
            "status": None,
        }],
    }
    assert not (Path(tmp_path) / "CalendarioAsismetro.ics").exists()


def test_get_optional_calendar_returns_none_when_agenda_is_missing(tmp_path, monkeypatch):
    driver = Mock()
    monkeypatch.setattr(calendar_action, "DOWNLOAD_DIR", str(tmp_path))
    search = Mock(return_value=None)
    monkeypatch.setattr(calendar_action, "search_element", search)

    returned_driver, calendar = calendar_action.get_calendar(driver, optional=True)

    assert returned_driver is driver
    assert calendar is None
    assert search.call_args.kwargs["raise_exception"] is False


@pytest.mark.parametrize("optional", [False, True])
def test_calendar_without_download_is_only_allowed_for_optional_month(tmp_path, monkeypatch, optional):
    driver = Mock()
    monkeypatch.setattr(calendar_action, "DOWNLOAD_DIR", str(tmp_path))
    monkeypatch.setattr(calendar_action, "DOWNLOAD_MAX_TIMEOUT", 0.1)
    monkeypatch.setattr(calendar_action, "search_element", Mock(return_value=object()))
    monkeypatch.setattr(calendar_action, "click_element", Mock(return_value=driver))
    # A previous export must never be returned as the new month's calendar.
    (tmp_path / "CalendarioAsismetro.ics").write_text("previous export", encoding="utf-8")

    if optional:
        assert calendar_action.get_calendar(driver, optional=True) == (driver, None)
    else:
        with pytest.raises(messageError, match="No se completó la descarga"):
            calendar_action.get_calendar(driver)

    assert not (tmp_path / "CalendarioAsismetro.ics").exists()


@pytest.mark.parametrize("optional", [False, True])
def test_html_only_export_is_not_returned_as_a_calendar(tmp_path, monkeypatch, optional):
    driver = Mock()
    monkeypatch.setattr(calendar_action, "DOWNLOAD_DIR", str(tmp_path))
    monkeypatch.setattr(calendar_action, "search_element", Mock(return_value=object()))

    def click_and_download_html(current_driver, button):
        (tmp_path / "CalendarioAsismetro.ics").write_text("<div>Inicio</div>", encoding="utf-8")
        return current_driver

    monkeypatch.setattr(calendar_action, "click_element", click_and_download_html)

    if optional:
        assert calendar_action.get_calendar(driver, optional=True) == (driver, None)
    else:
        with pytest.raises(messageError, match="no contiene un calendario"):
            calendar_action.get_calendar(driver)
