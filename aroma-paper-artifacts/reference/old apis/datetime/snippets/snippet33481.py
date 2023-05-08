from datetime import datetime, timedelta, tzinfo
from bisect import bisect_right
import pytz
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError
from sets import Set as set


def localize(self, dt, is_dst=False):
    'Convert naive time to local time'
    if (dt.tzinfo is not None):
        raise ValueError('Not naive datetime (tzinfo is already set)')
    return dt.replace(tzinfo=self)
