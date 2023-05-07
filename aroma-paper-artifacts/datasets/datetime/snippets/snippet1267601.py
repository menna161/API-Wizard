from datetime import datetime, timedelta, tzinfo
from bisect import bisect_right
import pytz
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError
from sets import Set as set


def memorized_datetime(seconds):
    'Create only one instance of each distinct datetime'
    try:
        return _datetime_cache[seconds]
    except KeyError:
        dt = (_epoch + timedelta(seconds=seconds))
        _datetime_cache[seconds] = dt
        return dt
