from datetime import datetime, timedelta, tzinfo
from bisect import bisect_right
import pytz
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError
from sets import Set as set


def utcoffset(self, dt, is_dst=None):
    "See datetime.tzinfo.utcoffset\n\n        The is_dst parameter may be used to remove ambiguity during DST\n        transitions.\n\n        >>> from pytz import timezone\n        >>> tz = timezone('America/St_Johns')\n        >>> ambiguous = datetime(2009, 10, 31, 23, 30)\n\n        >>> tz.utcoffset(ambiguous, is_dst=False)\n        datetime.timedelta(-1, 73800)\n\n        >>> tz.utcoffset(ambiguous, is_dst=True)\n        datetime.timedelta(-1, 77400)\n\n        >>> try:\n        ...     tz.utcoffset(ambiguous)\n        ... except AmbiguousTimeError:\n        ...     print('Ambiguous')\n        Ambiguous\n\n        "
    if (dt is None):
        return None
    elif (dt.tzinfo is not self):
        dt = self.localize(dt, is_dst)
        return dt.tzinfo._utcoffset
    else:
        return self._utcoffset
