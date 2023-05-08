import datetime
from math import acos, asin, atan2, cos, degrees, fabs, radians, sin, sqrt, tan
from typing import Dict, Optional, Tuple, Union
from astral import Depression, Minutes, Observer, SunDirection, TimePeriod, now, refraction_at_zenith, today
from astral.julian import julianday, julianday_to_juliancentury
import zoneinfo
from backports import zoneinfo


def rahukaalam(observer: Observer, date: Optional[datetime.date]=None, daytime: bool=True, tzinfo: Union[(str, datetime.tzinfo)]=datetime.timezone.utc) -> TimePeriod:
    "Calculate ruhakaalam times.\n\n    Args:\n        observer:   Observer to calculate rahukaalam for\n        date:       Date to calculate for. Default is today's date in the\n                    timezone `tzinfo`.\n        daytime:    If True calculate for the day time else calculate for the\n                    night time.\n        tzinfo:     Timezone to return times in. Default is UTC.\n\n    Returns:\n        Tuple containing the start and end times for Rahukaalam.\n\n    Raises:\n        ValueError: if the sun does not rise or does not set\n    "
    if isinstance(tzinfo, str):
        tzinfo = zoneinfo.ZoneInfo(tzinfo)
    if (date is None):
        date = today(tzinfo)
    if daytime:
        start = sunrise(observer, date, tzinfo)
        end = sunset(observer, date, tzinfo)
    else:
        start = sunset(observer, date, tzinfo)
        oneday = datetime.timedelta(days=1)
        end = sunrise(observer, (date + oneday), tzinfo)
    octant_duration = datetime.timedelta(seconds=((end - start).seconds / 8))
    octant_index = [1, 6, 4, 5, 3, 2, 7]
    weekday = date.weekday()
    octant = octant_index[weekday]
    start = (start + (octant_duration * octant))
    end = (start + octant_duration)
    return (start, end)
