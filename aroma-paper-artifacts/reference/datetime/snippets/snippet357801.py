import datetime
from math import acos, asin, atan2, cos, degrees, fabs, radians, sin, sqrt, tan
from typing import Dict, Optional, Tuple, Union
from astral import Depression, Minutes, Observer, SunDirection, TimePeriod, now, refraction_at_zenith, today
from astral.julian import julianday, julianday_to_juliancentury
import zoneinfo
from backports import zoneinfo


def noon(observer: Observer, date: Optional[datetime.date]=None, tzinfo: Union[(str, datetime.tzinfo)]=datetime.timezone.utc) -> datetime.datetime:
    'Calculate solar noon time when the sun is at its highest point.\n\n    Args:\n        observer: An observer viewing the sun at a specific, latitude, longitude\n                  and elevation\n        date:     Date to calculate for. Default is today for the specified tzinfo.\n        tzinfo:   Timezone to return times in. Default is UTC.\n\n    Returns:\n        Date and time at which noon occurs.\n    '
    if isinstance(tzinfo, str):
        tzinfo = zoneinfo.ZoneInfo(tzinfo)
    if (date is None):
        date = today(tzinfo)
    jc = julianday_to_juliancentury(julianday(date))
    eqtime = eq_of_time(jc)
    timeUTC = (((720.0 - (4 * observer.longitude)) - eqtime) / 60.0)
    hour = int(timeUTC)
    minute = int(((timeUTC - hour) * 60))
    second = int(((((timeUTC - hour) * 60) - minute) * 60))
    if (second > 59):
        second -= 60
        minute += 1
    elif (second < 0):
        second += 60
        minute -= 1
    if (minute > 59):
        minute -= 60
        hour += 1
    elif (minute < 0):
        minute += 60
        hour -= 1
    if (hour > 23):
        hour -= 24
        date += datetime.timedelta(days=1)
    elif (hour < 0):
        hour += 24
        date -= datetime.timedelta(days=1)
    noon = datetime.datetime(date.year, date.month, date.day, hour, minute, second, tzinfo=datetime.timezone.utc)
    return noon.astimezone(tzinfo)
