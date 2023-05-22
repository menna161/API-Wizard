from datetime import datetime, timedelta, tzinfo
from bisect import bisect_right
import pytz
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError
from sets import Set as set


def fromutc(self, dt):
    'See datetime.tzinfo.fromutc'
    if ((dt.tzinfo is not None) and (getattr(dt.tzinfo, '_tzinfos', None) is not self._tzinfos)):
        raise ValueError('fromutc: dt.tzinfo is not self')
    dt = dt.replace(tzinfo=None)
    idx = max(0, (bisect_right(self._utc_transition_times, dt) - 1))
    inf = self._transition_info[idx]
    return (dt + inf[0]).replace(tzinfo=self._tzinfos[inf])
