from datetime import datetime, timedelta, tzinfo
from bisect import bisect_right
import pytz
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError
from sets import Set as set


def tzname(self, dt, is_dst=None):
    'See datetime.tzinfo.tzname\n\n        is_dst is ignored for StaticTzInfo, and exists only to\n        retain compatibility with DstTzInfo.\n        '
    return self._tzname
