import datetime
from math import acos, asin, atan2, cos, degrees, fabs, radians, sin, sqrt, tan
from typing import Dict, Optional, Tuple, Union
from astral import Depression, Minutes, Observer, SunDirection, TimePeriod, now, refraction_at_zenith, today
from astral.julian import julianday, julianday_to_juliancentury
import zoneinfo
from backports import zoneinfo


def dawn(observer: Observer, date: Optional[datetime.date]=None, depression: Union[(float, Depression)]=Depression.CIVIL, tzinfo: Union[(str, datetime.tzinfo)]=datetime.timezone.utc) -> datetime.datetime:
    "Calculate dawn time.\n\n    Args:\n        observer:   Observer to calculate dawn for\n        date:       Date to calculate for. Default is today's date in the\n                    timezone `tzinfo`.\n        depression: Number of degrees below the horizon to use to calculate dawn.\n                    Default is for Civil dawn i.e. 6.0\n        tzinfo:     Timezone to return times in. Default is UTC.\n\n    Returns:\n        Date and time at which dawn occurs.\n\n    Raises:\n        ValueError: if dawn does not occur on the specified date\n    "
    if isinstance(tzinfo, str):
        tzinfo = zoneinfo.ZoneInfo(tzinfo)
    if (date is None):
        date = today(tzinfo)
    elif isinstance(date, datetime.datetime):
        tzinfo = (date.tzinfo or tzinfo)
        date = date.date()
    dep: float = 0.0
    if isinstance(depression, Depression):
        dep = depression.value
    else:
        dep = depression
    try:
        tot = time_of_transit(observer, date, (90.0 + dep), SunDirection.RISING).astimezone(tzinfo)
        tot_date = tot.date()
        if (tot_date != date):
            if (tot_date < date):
                delta = datetime.timedelta(days=1)
            else:
                delta = datetime.timedelta(days=(- 1))
            new_date = (date + delta)
            tot = time_of_transit(observer, new_date, (90.0 + dep), SunDirection.RISING).astimezone(tzinfo)
            tot_date = tot.date()
            if (tot_date != date):
                raise ValueError('Unable to find a dawn time on the date specified')
        return tot
    except ValueError as exc:
        if (exc.args[0] == 'math domain error'):
            raise ValueError(f'Sun never reaches {dep} degrees below the horizon, at this location.') from exc
        else:
            raise
