from datetime import datetime, timedelta, tzinfo
from bisect import bisect_right
import pytz
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError
from sets import Set as set


def normalize(self, dt, is_dst=False):
    "Correct the timezone information on the given datetime.\n\n        This is normally a no-op, as StaticTzInfo timezones never have\n        ambiguous cases to correct:\n\n        >>> from pytz import timezone\n        >>> gmt = timezone('GMT')\n        >>> isinstance(gmt, StaticTzInfo)\n        True\n        >>> dt = datetime(2011, 5, 8, 1, 2, 3, tzinfo=gmt)\n        >>> gmt.normalize(dt) is dt\n        True\n\n        The supported method of converting between timezones is to use\n        datetime.astimezone(). Currently normalize() also works:\n\n        >>> la = timezone('America/Los_Angeles')\n        >>> dt = la.localize(datetime(2011, 5, 7, 1, 2, 3))\n        >>> fmt = '%Y-%m-%d %H:%M:%S %Z (%z)'\n        >>> gmt.normalize(dt).strftime(fmt)\n        '2011-05-07 08:02:03 GMT (+0000)'\n        "
    if (dt.tzinfo is self):
        return dt
    if (dt.tzinfo is None):
        raise ValueError('Naive time - no tzinfo set')
    return dt.astimezone(self)
