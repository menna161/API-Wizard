import datetime
from math import acos, asin, atan2, cos, degrees, fabs, radians, sin, sqrt, tan
from typing import Dict, Optional, Tuple, Union
from astral import Depression, Minutes, Observer, SunDirection, TimePeriod, now, refraction_at_zenith, today
from astral.julian import julianday, julianday_to_juliancentury
import zoneinfo
from backports import zoneinfo


def time_of_transit(observer: Observer, date: datetime.date, zenith: float, direction: SunDirection, with_refraction: bool=True) -> datetime.datetime:
    'Calculate the time in the UTC timezone when the sun transits the\n    specificed zenith\n\n    Args:\n        observer: An observer viewing the sun at a specific, latitude, longitude\n            and elevation\n        date: The date to calculate for\n        zenith: The zenith angle for which to calculate the transit time\n        direction: The direction that the sun is traversing\n\n    Raises:\n        ValueError if the zenith is not transitted by the sun\n\n    Returns:\n        the time when the sun transits the specificed zenith\n    '
    if (observer.latitude > 89.8):
        latitude = 89.8
    elif (observer.latitude < (- 89.8)):
        latitude = (- 89.8)
    else:
        latitude = observer.latitude
    adjustment_for_elevation = 0.0
    if (isinstance(observer.elevation, float) and (observer.elevation > 0.0)):
        adjustment_for_elevation = adjust_to_horizon(observer.elevation)
    elif isinstance(observer.elevation, tuple):
        adjustment_for_elevation = adjust_to_obscuring_feature(observer.elevation)
    if with_refraction:
        adjustment_for_refraction = refraction_at_zenith((zenith + adjustment_for_elevation))
    else:
        adjustment_for_refraction = 0.0
    jd = julianday(date)
    adjustment = 0.0
    timeUTC = 0.0
    for _ in range(2):
        jc = julianday_to_juliancentury((jd + adjustment))
        declination = sun_declination(jc)
        hourangle = hour_angle(latitude, declination, ((zenith + adjustment_for_elevation) + adjustment_for_refraction), direction)
        delta = ((- observer.longitude) - degrees(hourangle))
        eqtime = eq_of_time(jc)
        offset = ((delta * 4.0) - eqtime)
        if (offset < (- 720.0)):
            offset += 1440
        timeUTC = (720.0 + offset)
        adjustment = (timeUTC / 1440.0)
    td = minutes_to_timedelta(timeUTC)
    dt = (datetime.datetime(date.year, date.month, date.day) + td)
    dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt
