import datetime
from math import acos, asin, atan2, cos, degrees, fabs, radians, sin, sqrt, tan
from typing import Dict, Optional, Tuple, Union
from astral import Depression, Minutes, Observer, SunDirection, TimePeriod, now, refraction_at_zenith, today
from astral.julian import julianday, julianday_to_juliancentury
import zoneinfo
from backports import zoneinfo


def midnight(observer: Observer, date: Optional[datetime.date]=None, tzinfo: Union[(str, datetime.tzinfo)]=datetime.timezone.utc) -> datetime.datetime:
    'Calculate solar midnight time.\n\n    Note:\n        This calculates the solar midnight that is closest\n        to 00:00:00 of the specified date i.e. it may return a time that is on\n        the previous day.\n\n    Args:\n        observer: An observer viewing the sun at a specific, latitude, longitude\n                  and elevation\n        date:     Date to calculate for. Default is today for the specified tzinfo.\n        tzinfo:   Timezone to return times in. Default is UTC.\n\n    Returns:\n        Date and time at which midnight occurs.\n    '
    if isinstance(tzinfo, str):
        tzinfo = zoneinfo.ZoneInfo(tzinfo)
    if (date is None):
        date = today(tzinfo)
    midday = datetime.time(12, 0, 0)
    jd = julianday(datetime.datetime.combine(date, midday))
    newt = julianday_to_juliancentury(((jd + 0.5) + ((- observer.longitude) / 360.0)))
    eqtime = eq_of_time(newt)
    timeUTC = (((- observer.longitude) * 4.0) - eqtime)
    timeUTC = (timeUTC / 60.0)
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
    if (hour < 0):
        hour += 24
        date -= datetime.timedelta(days=1)
    midnight = datetime.datetime(date.year, date.month, date.day, hour, minute, second, tzinfo=datetime.timezone.utc)
    return midnight.astimezone(tzinfo)
