from datetime import datetime, timedelta, tzinfo
from bisect import bisect_right
import pytz
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError
from sets import Set as set


def normalize(self, dt):
    "Correct the timezone information on the given datetime\n\n        If date arithmetic crosses DST boundaries, the tzinfo\n        is not magically adjusted. This method normalizes the\n        tzinfo to the correct one.\n\n        To test, first we need to do some setup\n\n        >>> from pytz import timezone\n        >>> utc = timezone('UTC')\n        >>> eastern = timezone('US/Eastern')\n        >>> fmt = '%Y-%m-%d %H:%M:%S %Z (%z)'\n\n        We next create a datetime right on an end-of-DST transition point,\n        the instant when the wallclocks are wound back one hour.\n\n        >>> utc_dt = datetime(2002, 10, 27, 6, 0, 0, tzinfo=utc)\n        >>> loc_dt = utc_dt.astimezone(eastern)\n        >>> loc_dt.strftime(fmt)\n        '2002-10-27 01:00:00 EST (-0500)'\n\n        Now, if we subtract a few minutes from it, note that the timezone\n        information has not changed.\n\n        >>> before = loc_dt - timedelta(minutes=10)\n        >>> before.strftime(fmt)\n        '2002-10-27 00:50:00 EST (-0500)'\n\n        But we can fix that by calling the normalize method\n\n        >>> before = eastern.normalize(before)\n        >>> before.strftime(fmt)\n        '2002-10-27 01:50:00 EDT (-0400)'\n\n        The supported method of converting between timezones is to use\n        datetime.astimezone(). Currently, normalize() also works:\n\n        >>> th = timezone('Asia/Bangkok')\n        >>> am = timezone('Europe/Amsterdam')\n        >>> dt = th.localize(datetime(2011, 5, 7, 1, 2, 3))\n        >>> fmt = '%Y-%m-%d %H:%M:%S %Z (%z)'\n        >>> am.normalize(dt).strftime(fmt)\n        '2011-05-06 20:02:03 CEST (+0200)'\n        "
    if (dt.tzinfo is None):
        raise ValueError('Naive time - no tzinfo set')
    offset = dt.tzinfo._utcoffset
    dt = dt.replace(tzinfo=None)
    dt = (dt - offset)
    return self.fromutc(dt)
