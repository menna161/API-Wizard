import datetime
from enum import Enum
from typing import Union


def julianday_2000(at: Union[(datetime.datetime, datetime.date)]) -> float:
    'Calculate the numer of Julian Days since Jan 1.5, 2000'
    return (julianday(at) - 2451545.0)
