import datetime
from math import acos, asin, atan2, cos, degrees, fabs, radians, sin, sqrt, tan
from typing import Dict, Optional, Tuple, Union
from astral import Depression, Minutes, Observer, SunDirection, TimePeriod, now, refraction_at_zenith, today
from astral.julian import julianday, julianday_to_juliancentury
import zoneinfo
from backports import zoneinfo


def time_at_elevation(observer: Observer, elevation: float, date: Optional[datetime.date]=None, direction: SunDirection=SunDirection.RISING, tzinfo: Union[(str, datetime.tzinfo)]=datetime.timezone.utc, with_refraction: bool=True) -> datetime.datetime:
    "Calculates the time when the sun is at the specified elevation on the\n    specified date.\n\n    Note:\n        This method uses positive elevations for those above the horizon.\n\n        Elevations greater than 90 degrees are converted to a setting sun\n        i.e. an elevation of 110 will calculate a setting sun at 70 degrees.\n\n    Args:\n        elevation: Elevation of the sun in degrees above the horizon to calculate for.\n        observer:  Observer to calculate for\n        date:      Date to calculate for. Default is today's date in the timezone\n                   `tzinfo`.\n        direction: Determines whether the calculated time is for the sun rising\n                   or setting.\n                   Use ``SunDirection.RISING`` or ``SunDirection.SETTING``.\n                   Default is rising.\n        tzinfo:    Timezone to return times in. Default is UTC.\n\n    Returns:\n        Date and time at which the sun is at the specified elevation.\n    "
    if (elevation > 90.0):
        elevation = (180.0 - elevation)
        direction = SunDirection.SETTING
    if isinstance(tzinfo, str):
        tzinfo = zoneinfo.ZoneInfo(tzinfo)
    if (date is None):
        date = today(tzinfo)
    zenith = (90 - elevation)
    try:
        return time_of_transit(observer, date, zenith, direction, with_refraction).astimezone(tzinfo)
    except ValueError as exc:
        if (exc.args[0] == 'math domain error'):
            raise ValueError(f'Sun never reaches an elevation of {elevation} degrees at this location.') from exc
        else:
            raise
