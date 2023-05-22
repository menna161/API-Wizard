from datetime import datetime, timedelta, tzinfo
from bisect import bisect_right
import pytz
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError
from sets import Set as set


def tzname(self, dt, is_dst=None):
    "See datetime.tzinfo.tzname\n\n        The is_dst parameter may be used to remove ambiguity during DST\n        transitions.\n\n        >>> from pytz import timezone\n        >>> tz = timezone('America/St_Johns')\n\n        >>> normal = datetime(2009, 9, 1)\n\n        >>> tz.tzname(normal)\n        'NDT'\n        >>> tz.tzname(normal, is_dst=False)\n        'NDT'\n        >>> tz.tzname(normal, is_dst=True)\n        'NDT'\n\n        >>> ambiguous = datetime(2009, 10, 31, 23, 30)\n\n        >>> tz.tzname(ambiguous, is_dst=False)\n        'NST'\n        >>> tz.tzname(ambiguous, is_dst=True)\n        'NDT'\n        >>> try:\n        ...     tz.tzname(ambiguous)\n        ... except AmbiguousTimeError:\n        ...     print('Ambiguous')\n        Ambiguous\n        "
    if (dt is None):
        return self.zone
    elif (dt.tzinfo is not self):
        dt = self.localize(dt, is_dst)
        return dt.tzinfo._tzname
    else:
        return self._tzname
