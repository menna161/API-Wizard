import datetime
from math import acos, asin, atan2, cos, degrees, fabs, radians, sin, sqrt, tan
from typing import Dict, Optional, Tuple, Union
from astral import Depression, Minutes, Observer, SunDirection, TimePeriod, now, refraction_at_zenith, today
from astral.julian import julianday, julianday_to_juliancentury
import zoneinfo
from backports import zoneinfo


def daylight(observer: Observer, date: Optional[datetime.date]=None, tzinfo: Union[(str, datetime.tzinfo)]=datetime.timezone.utc) -> TimePeriod:
    "Calculate daylight start and end times.\n\n    Args:\n        observer:   Observer to calculate daylight for\n        date:       Date to calculate for. Default is today's date in the\n                    timezone `tzinfo`.\n        tzinfo:     Timezone to return times in. Default is UTC.\n\n    Returns:\n        A tuple of the date and time at which daylight starts and ends.\n\n    Raises:\n        ValueError: if the sun does not rise or does not set\n    "
    if isinstance(tzinfo, str):
        tzinfo = zoneinfo.ZoneInfo(tzinfo)
    if (date is None):
        date = today(tzinfo)
    sr = sunrise(observer, date, tzinfo)
    ss = sunset(observer, date, tzinfo)
    return (sr, ss)
