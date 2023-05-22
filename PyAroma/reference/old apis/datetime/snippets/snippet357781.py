import datetime
from math import acos, asin, atan2, cos, degrees, fabs, radians, sin, sqrt, tan
from typing import Dict, Optional, Tuple, Union
from astral import Depression, Minutes, Observer, SunDirection, TimePeriod, now, refraction_at_zenith, today
from astral.julian import julianday, julianday_to_juliancentury
import zoneinfo
from backports import zoneinfo


def minutes_to_timedelta(minutes: float) -> datetime.timedelta:
    'Convert a floating point number of minutes to a\n    :class:`~datetime.timedelta`\n    '
    d = int((minutes / 1440))
    minutes = (minutes - (d * 1440))
    minutes = (minutes * 60)
    s = int(minutes)
    sfrac = (minutes - s)
    us = int((sfrac * 1000000))
    return datetime.timedelta(days=d, seconds=s, microseconds=us)
