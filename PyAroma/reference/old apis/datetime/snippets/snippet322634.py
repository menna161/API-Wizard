import datetime
import math
import re
import sys
import doctest


def glot_to_gpst(gpst_current_epoch, tod_seconds):
    '\n    Converts GLOT to GPST\n    :param gpst_current_epoch: Current epoch of the measurement in GPST\n    :param tod_seconds: Time of days as number of seconds\n    :return: Time of week in seconds\n    '
    (tod_sec_frac, tod_sec) = math.modf(tod_seconds)
    tod_sec = int(tod_sec)
    glo_epoch = (datetime.datetime(year=gpst_current_epoch.year, month=gpst_current_epoch.month, day=gpst_current_epoch.day, hour=gpst_current_epoch.hour, minute=gpst_current_epoch.minute, second=gpst_current_epoch.second) + datetime.timedelta(hours=3, seconds=(- CURRENT_GPS_LEAP_SECOND)))
    glo_tod = (datetime.datetime(year=glo_epoch.year, month=glo_epoch.month, day=glo_epoch.day) + datetime.timedelta(seconds=tod_sec))
    day_of_week_sec = (glo_tod.isoweekday() * DAYSEC)
    tow_sec = (((day_of_week_sec + tod_seconds) - GLOT_TO_UTC) + CURRENT_GPS_LEAP_SECOND)
    return tow_sec
