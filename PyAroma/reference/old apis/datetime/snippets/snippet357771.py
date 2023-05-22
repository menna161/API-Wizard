import datetime
from dataclasses import dataclass, field, replace
from math import asin, atan2, cos, degrees, fabs, pi, radians, sin, sqrt
from typing import Callable, List, Optional, Union
from astral import AstralBodyPosition, Observer, now, today
from astral.julian import julianday, julianday_2000
from astral.sidereal import lmst
from astral.table4 import Table4Row, table4_u, table4_v, table4_w
import zoneinfo
from backports import zoneinfo


def moonrise(observer: Observer, date: Optional[datetime.date]=None, tzinfo: Union[(str, datetime.tzinfo)]=datetime.timezone.utc) -> Optional[datetime.datetime]:
    "Calculate the moon rise time\n\n    Args:\n        observer: Observer to calculate moonrise for\n        date:     Date to calculate for. Default is today's date in the\n                  timezone `tzinfo`.\n        tzinfo:   Timezone to return times in. Default is UTC.\n\n    Returns:\n        Date and time at which moonrise occurs.\n    "
    if isinstance(tzinfo, str):
        tzinfo = zoneinfo.ZoneInfo(tzinfo)
    if (date is None):
        date = today(tzinfo)
    elif isinstance(date, datetime.datetime):
        date = date.date()
    info = riseset(date, observer)
    if info[0]:
        rise = info[0].astimezone(tzinfo)
        rd = rise.date()
        if (rd != date):
            if (rd > date):
                delta = datetime.timedelta(days=(- 1))
            else:
                delta = datetime.timedelta(days=1)
            new_date = (date + delta)
            info = riseset(new_date, observer)
            if info[0]:
                rise = info[0].astimezone(tzinfo)
                rd = rise.date()
                if (rd != date):
                    rise = None
        return rise
    else:
        raise ValueError('Moon never rises on this date, at this location')