import datetime
from math import acos, asin, atan2, cos, degrees, fabs, radians, sin, sqrt, tan
from typing import Dict, Optional, Tuple, Union
from astral import Depression, Minutes, Observer, SunDirection, TimePeriod, now, refraction_at_zenith, today
from astral.julian import julianday, julianday_to_juliancentury
import zoneinfo
from backports import zoneinfo


def zenith_and_azimuth(observer: Observer, dateandtime: datetime.datetime, with_refraction: bool=True) -> Tuple[(float, float)]:
    if (observer.latitude > 89.8):
        latitude = 89.8
    elif (observer.latitude < (- 89.8)):
        latitude = (- 89.8)
    else:
        latitude = observer.latitude
    longitude = observer.longitude
    if (dateandtime.tzinfo is None):
        zone = 0.0
        utc_datetime = dateandtime
    else:
        zone = ((- dateandtime.utcoffset().total_seconds()) / 3600.0)
        utc_datetime = dateandtime.astimezone(datetime.timezone.utc)
    jd = julianday(utc_datetime)
    t = julianday_to_juliancentury(jd)
    declination = sun_declination(t)
    eqtime = eq_of_time(t)
    solarTimeFix = ((eqtime + (4.0 * longitude)) + (60 * zone))
    trueSolarTime = ((((dateandtime.hour * 60.0) + dateandtime.minute) + (dateandtime.second / 60.0)) + solarTimeFix)
    while (trueSolarTime > 1440):
        trueSolarTime = (trueSolarTime - 1440)
    hourangle = ((trueSolarTime / 4.0) - 180.0)
    if (hourangle < (- 180)):
        hourangle = (hourangle + 360.0)
    ch = cos(radians(hourangle))
    cl = cos(radians(latitude))
    sl = sin(radians(latitude))
    sd = sin(radians(declination))
    cd = cos(radians(declination))
    csz = (((cl * cd) * ch) + (sl * sd))
    if (csz > 1.0):
        csz = 1.0
    elif (csz < (- 1.0)):
        csz = (- 1.0)
    zenith = degrees(acos(csz))
    azDenom = (cl * sin(radians(zenith)))
    if (abs(azDenom) > 0.001):
        azRad = (((sl * cos(radians(zenith))) - sd) / azDenom)
        if (abs(azRad) > 1.0):
            if (azRad < 0):
                azRad = (- 1.0)
            else:
                azRad = 1.0
        azimuth = (180.0 - degrees(acos(azRad)))
        if (hourangle > 0.0):
            azimuth = (- azimuth)
    elif (latitude > 0.0):
        azimuth = 180.0
    else:
        azimuth = 0.0
    if (azimuth < 0.0):
        azimuth = (azimuth + 360.0)
    if with_refraction:
        zenith -= refraction_at_zenith(zenith)
    return (zenith, azimuth)
