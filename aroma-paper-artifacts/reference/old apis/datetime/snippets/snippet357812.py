import datetime
from math import acos, asin, atan2, cos, degrees, fabs, radians, sin, sqrt, tan
from typing import Dict, Optional, Tuple, Union
from astral import Depression, Minutes, Observer, SunDirection, TimePeriod, now, refraction_at_zenith, today
from astral.julian import julianday, julianday_to_juliancentury
import zoneinfo
from backports import zoneinfo


def night(observer: Observer, date: Optional[datetime.date]=None, tzinfo: Union[(str, datetime.tzinfo)]=datetime.timezone.utc) -> TimePeriod:
    "Calculate night start and end times.\n\n    Night is calculated to be between astronomical dusk on the\n    date specified and astronomical dawn of the next day.\n\n    Args:\n        observer:   Observer to calculate night for\n        date:       Date to calculate for. Default is today's date for the\n                    specified tzinfo.\n        tzinfo:     Timezone to return times in. Default is UTC.\n\n    Returns:\n        A tuple of the date and time at which night starts and ends.\n\n    Raises:\n        ValueError: if dawn does not occur on the specified date or\n                    dusk on the following day\n    "
    if isinstance(tzinfo, str):
        tzinfo = zoneinfo.ZoneInfo(tzinfo)
    if (date is None):
        date = today(tzinfo)
    start = dusk(observer, date, 6, tzinfo)
    tomorrow = (date + datetime.timedelta(days=1))
    end = dawn(observer, tomorrow, 6, tzinfo)
    return (start, end)
