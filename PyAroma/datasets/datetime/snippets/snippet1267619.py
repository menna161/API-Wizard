from datetime import datetime, timedelta, tzinfo
from bisect import bisect_right
import pytz
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError
from sets import Set as set


def dst(self, dt, is_dst=None):
    "See datetime.tzinfo.dst\n\n        The is_dst parameter may be used to remove ambiguity during DST\n        transitions.\n\n        >>> from pytz import timezone\n        >>> tz = timezone('America/St_Johns')\n\n        >>> normal = datetime(2009, 9, 1)\n\n        >>> str(tz.dst(normal))\n        '1:00:00'\n        >>> str(tz.dst(normal, is_dst=False))\n        '1:00:00'\n        >>> str(tz.dst(normal, is_dst=True))\n        '1:00:00'\n\n        >>> ambiguous = datetime(2009, 10, 31, 23, 30)\n\n        >>> str(tz.dst(ambiguous, is_dst=False))\n        '0:00:00'\n        >>> str(tz.dst(ambiguous, is_dst=True))\n        '1:00:00'\n        >>> try:\n        ...     tz.dst(ambiguous)\n        ... except AmbiguousTimeError:\n        ...     print('Ambiguous')\n        Ambiguous\n\n        "
    if (dt is None):
        return None
    elif (dt.tzinfo is not self):
        dt = self.localize(dt, is_dst)
        return dt.tzinfo._dst
    else:
        return self._dst
