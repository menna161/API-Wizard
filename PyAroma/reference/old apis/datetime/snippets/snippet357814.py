import datetime
from math import acos, asin, atan2, cos, degrees, fabs, radians, sin, sqrt, tan
from typing import Dict, Optional, Tuple, Union
from astral import Depression, Minutes, Observer, SunDirection, TimePeriod, now, refraction_at_zenith, today
from astral.julian import julianday, julianday_to_juliancentury
import zoneinfo
from backports import zoneinfo


def golden_hour(observer: Observer, date: Optional[datetime.date]=None, direction: SunDirection=SunDirection.RISING, tzinfo: Union[(str, datetime.tzinfo)]=datetime.timezone.utc) -> TimePeriod:
    "Returns the start and end times of the Golden Hour\n    when the sun is traversing in the specified direction.\n\n    This method uses the definition from PhotoPills i.e. the\n    golden hour is when the sun is between 4 degrees below the horizon\n    and 6 degrees above.\n\n    Args:\n        observer:   Observer to calculate the golden hour for\n        date:       Date for which to calculate the times.\n                    Default is today's date in the timezone `tzinfo`.\n        direction:  Determines whether the time is for the sun rising or setting.\n                    Use ``SunDirection.RISING`` or ``SunDirection.SETTING``.\n        tzinfo:     Timezone to return times in. Default is UTC.\n\n    Returns:\n        A tuple of the date and time at which the Golden Hour starts and ends.\n\n    Raises:\n        ValueError: if the sun does not transit the elevations -4 & +6 degrees\n    "
    if isinstance(tzinfo, str):
        tzinfo = zoneinfo.ZoneInfo(tzinfo)
    if (date is None):
        date = today(tzinfo)
    start = time_of_transit(observer, date, (90 + 4), direction).astimezone(tzinfo)
    end = time_of_transit(observer, date, (90 - 6), direction).astimezone(tzinfo)
    if (direction == SunDirection.RISING):
        return (start, end)
    else:
        return (end, start)
