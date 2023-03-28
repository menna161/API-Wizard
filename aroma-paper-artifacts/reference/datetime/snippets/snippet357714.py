import datetime
from enum import Enum
from typing import Union


def julianday_to_datetime(jd: float) -> datetime.datetime:
    'Convert a Julian Day number to a datetime'
    jd += 0.5
    z = int(jd)
    f = (jd - z)
    if (z < 2299161):
        a = z
    else:
        alpha = int(((z - 1867216.25) / 36524.25))
        a = (((z + 1) + alpha) + int((alpha / 4.0)))
    b = (a + 1524)
    c = int(((b - 122.1) / 365.25))
    d = int((365.25 * c))
    e = int(((b - d) / 30.6001))
    d = (((b - d) - int((30.6001 * e))) + f)
    day = int(d)
    t = (d - day)
    total_seconds = (t * ((24 * 60) * 60))
    hour = int((total_seconds / 3600))
    total_seconds -= (hour * 3600)
    minute = int((total_seconds / 60))
    total_seconds -= (minute * 60)
    seconds = int(total_seconds)
    if (e < 14):
        month = (e - 1)
    else:
        month = (e - 13)
    if (month > 2):
        year = (c - 4716)
    else:
        year = (c - 4715)
    return datetime.datetime(year, month, day, hour, minute, seconds)
