import datetime
from enum import Enum
from typing import Union


def julianday_modified(at: datetime.datetime) -> float:
    'Calculate the Modified Julian Date number'
    year = at.year
    month = at.month
    day = at.day
    a = (((10000 * year) + (100 * month)) + day)
    if (year < 0):
        year += 1
    if (month <= 2):
        month += 12
        year -= 1
    if (a <= 15821004.1):
        b = (((- 2) + ((year + 4716) / 4)) - 1179)
    else:
        b = (((year / 400) - (year / 100)) + (year / 4))
    a = ((365 * year) - 679004)
    mjd = ((((a + b) + int((30.6001 * (month + 1)))) + day) + (at.hour / 24))
    return mjd
