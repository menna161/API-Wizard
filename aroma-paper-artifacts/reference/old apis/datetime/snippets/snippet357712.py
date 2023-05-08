import datetime
from enum import Enum
from typing import Union


def julianday(at: Union[(datetime.datetime, datetime.date)], calendar: Calendar=Calendar.GREGORIAN) -> float:
    'Calculate the Julian Day (number) for the specified date/time\n\n    julian day numbers for dates are calculated for the start of the day\n    '

    def _time_to_seconds(t: datetime.time) -> int:
        return int((((t.hour * 3600) + (t.minute * 60)) + t.second))
    year = at.year
    month = at.month
    day = at.day
    day_fraction = 0.0
    if isinstance(at, datetime.datetime):
        t = _time_to_seconds(at.time())
        day_fraction = (t / ((24 * 60) * 60))
    else:
        day_fraction = 0.0
    if (month <= 2):
        year -= 1
        month += 12
    a = int((year / 100))
    if (calendar == Calendar.GREGORIAN):
        b = ((2 - a) + int((a / 4)))
    else:
        b = 0
    jd = (((((int((365.25 * (year + 4716))) + int((30.6001 * (month + 1)))) + day) + day_fraction) + b) - 1524.5)
    return jd
