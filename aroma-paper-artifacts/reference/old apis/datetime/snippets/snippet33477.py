from datetime import datetime, timedelta, tzinfo
from bisect import bisect_right
import pytz
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError
from sets import Set as set


def fromutc(self, dt):
    'See datetime.tzinfo.fromutc'
    if ((dt.tzinfo is not None) and (dt.tzinfo is not self)):
        raise ValueError('fromutc: dt.tzinfo is not self')
    return (dt + self._utcoffset).replace(tzinfo=self)
