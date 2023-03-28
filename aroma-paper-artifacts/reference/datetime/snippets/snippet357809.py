import datetime
from math import acos, asin, atan2, cos, degrees, fabs, radians, sin, sqrt, tan
from typing import Dict, Optional, Tuple, Union
from astral import Depression, Minutes, Observer, SunDirection, TimePeriod, now, refraction_at_zenith, today
from astral.julian import julianday, julianday_to_juliancentury
import zoneinfo
from backports import zoneinfo


def sunset(observer: Observer, date: Optional[datetime.date]=None, tzinfo: Union[(str, datetime.tzinfo)]=datetime.timezone.utc) -> datetime.datetime:
    "Calculate sunset time.\n\n    Args:\n        observer: Observer to calculate sunset for\n        date:     Date to calculate for. Default is today's date in the\n                  timezone `tzinfo`.\n        tzinfo:   Timezone to return times in. Default is UTC.\n\n    Returns:\n        Date and time at which sunset occurs.\n\n    Raises:\n        ValueError: if the sun does not reach the horizon\n    "
    if isinstance(tzinfo, str):
        tzinfo = zoneinfo.ZoneInfo(tzinfo)
    if (date is None):
        date = today(tzinfo)
    elif isinstance(date, datetime.datetime):
        tzinfo = (date.tzinfo or tzinfo)
        date = date.date()
    try:
        tot = time_of_transit(observer, date, (90.0 + SUN_APPARENT_RADIUS), SunDirection.SETTING).astimezone(tzinfo)
        tot_date = tot.date()
        if (tot_date != date):
            if (tot_date < date):
                delta = datetime.timedelta(days=1)
            else:
                delta = datetime.timedelta(days=(- 1))
            new_date = (date + delta)
            tot = time_of_transit(observer, new_date, (90.0 + SUN_APPARENT_RADIUS), SunDirection.SETTING).astimezone(tzinfo)
            tot_date = tot.date()
            if (tot_date != date):
                raise ValueError('Unable to find a sunset time on the date specified')
        return tot
    except ValueError as exc:
        if (exc.args[0] == 'math domain error'):
            z = zenith(observer, noon(observer, date))
            if (z > 90.0):
                msg = 'Sun is always below the horizon on this day, at this location.'
            else:
                msg = 'Sun is always above the horizon on this day, at this location.'
            raise ValueError(msg) from exc
        else:
            raise
