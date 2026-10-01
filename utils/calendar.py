import re
from datetime import date, datetime

from icalendar import Calendar

from utils.error import messageError


def parse_calendar_export(contents):
    """Parse the iCalendar block, excluding HTML emitted by AsisMetro."""
    match = re.search(
        r"^BEGIN:VCALENDAR\r?\n.*?^END:VCALENDAR[ \t]*(?:\r?\n|$)",
        contents,
        flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise messageError("El archivo descargado no contiene un calendario iCalendar válido")

    try:
        calendar = Calendar.from_ical(match.group(0))
    except Exception as error:
        raise messageError("No se pudo interpretar el calendario iCalendar descargado") from error

    if calendar.name != "VCALENDAR" or str(calendar.get("VERSION", "")) != "2.0":
        raise messageError("El archivo descargado no contiene un calendario iCalendar válido")
    if any(component.errors for component in calendar.walk()):
        raise messageError("El calendario iCalendar descargado contiene propiedades inválidas")

    return calendar


def calendar_to_json(calendar):
    """Return event data decoded from an iCalendar export."""
    def text_value(component, name):
        value = component.get(name)
        return str(value) if value is not None else None

    events = []
    for event in calendar.walk("VEVENT"):
        start = event.decoded("DTSTART", None)
        end = event.decoded("DTEND", None)
        if not isinstance(start, date):
            raise messageError("El calendario descargado contiene un evento sin fecha de inicio válida")
        if end is None and event.get("DURATION") is not None:
            end = start + event.decoded("DURATION")

        events.append({
            "uid": text_value(event, "UID"),
            "summary": text_value(event, "SUMMARY"),
            "description": text_value(event, "DESCRIPTION"),
            "location": text_value(event, "LOCATION"),
            "start": start.isoformat(),
            "end": end.isoformat() if end is not None else None,
            "all_day": not isinstance(start, datetime),
            "status": text_value(event, "STATUS"),
        })

    return {
        "name": text_value(calendar, "X-WR-CALNAME") or text_value(calendar, "NAME"),
        "timezone": text_value(calendar, "X-WR-TIMEZONE"),
        "events": events,
    }
