import datetime
from math import acos, asin, atan2, cos, degrees, fabs, radians, sin, sqrt, tan
from typing import Dict, Optional, Tuple, Union
from astral import Depression, Minutes, Observer, SunDirection, TimePeriod, now, refraction_at_zenith, today
from astral.julian import julianday, julianday_to_juliancentury
import zoneinfo
from backports import zoneinfo


def zenith(observer: Observer, dateandtime: Optional[datetime.datetime]=None, with_refraction: bool=True) -> float:
    'Calculate the zenith angle of the sun.\n\n    Args:\n        observer:    Observer to calculate the solar zenith for\n        dateandtime: The date and time for which to calculate the angle.\n                     If `dateandtime` is None or is a naive Python datetime\n                     then it is assumed to be in the UTC timezone.\n        with_refraction: If True adjust zenith to take refraction into account\n\n    Returns:\n        The zenith angle in degrees.\n    '
    if (dateandtime is None):
        dateandtime = now(datetime.timezone.utc)
    return zenith_and_azimuth(observer, dateandtime, with_refraction)[0]
