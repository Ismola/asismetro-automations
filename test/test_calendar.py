import pytest

from utils.calendar import calendar_to_json, parse_calendar_export
from utils.error import messageError


def test_export_excludes_html_and_preserves_calendar_properties():
    contents = (
        "<div>Inicio</div>\n"
        "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Calendar test//ES\n"
        "X-WR-CALNAME:Calendario de turnos\nX-WR-TIMEZONE:Europe/Madrid\n"
        "BEGIN:VEVENT\nUID:shift-1\nDTSTART;TZID=Europe/Madrid:20261010T090000\n"
        "DTEND;TZID=Europe/Madrid:20261010T120000\nSUMMARY:Turno de la ma\n ñana\n"
        "DESCRIPTION:Primera línea\\nSegunda línea\\, con coma\n"
        "END:VEVENT\nEND:VCALENDAR\n<div>Footer</div>"
    )

    calendar = parse_calendar_export(contents)
    event = calendar.walk("VEVENT")[0]

    assert str(calendar["X-WR-CALNAME"]) == "Calendario de turnos"
    assert str(event["SUMMARY"]) == "Turno de la mañana"
    assert str(event["DESCRIPTION"]) == "Primera línea\nSegunda línea, con coma"
    assert event.decoded("DTSTART").isoformat() == "2026-10-10T09:00:00+02:00"
    assert b"<div>" not in calendar.to_ical()
    result = calendar_to_json(calendar)
    assert result["name"] == "Calendario de turnos"
    assert result["timezone"] == "Europe/Madrid"
    assert result["events"][0]["start"] == "2026-10-10T09:00:00+02:00"
    assert result["events"][0]["end"] == "2026-10-10T12:00:00+02:00"
    assert result["events"][0]["description"] == "Primera línea\nSegunda línea, con coma"


def test_all_day_event_and_duration_are_decoded():
    calendar = parse_calendar_export(
        "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Calendar test//ES\n"
        "BEGIN:VEVENT\nUID:all-day\nDTSTART;VALUE=DATE:20261010\nDURATION:P1D\n"
        "SUMMARY:Turno\nEND:VEVENT\nEND:VCALENDAR\n"
    )

    event = calendar_to_json(calendar)["events"][0]

    assert event["all_day"] is True
    assert event["start"] == "2026-10-10"
    assert event["end"] == "2026-10-11"


def test_published_calendar_with_no_events_is_not_missing():
    calendar = parse_calendar_export(
        "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Calendar test//ES\nEND:VCALENDAR\n"
    )
    assert calendar_to_json(calendar)["events"] == []


@pytest.mark.parametrize("contents", [
    "<html><body>Calendario todavía no publicado</body></html>",
    "BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nDTSTART:invalid\nEND:VEVENT\nEND:VCALENDAR\n",
    "BEGIN:VCALENDAR\nVERSION:2.0\n",
])
def test_invalid_exports_are_rejected(contents):
    with pytest.raises(messageError):
        parse_calendar_export(contents)
