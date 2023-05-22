import sys
import datetime
import os.path
from pytz.exceptions import AmbiguousTimeError
from pytz.exceptions import InvalidTimeError
from pytz.exceptions import NonExistentTimeError
from pytz.exceptions import UnknownTimeZoneError
from pytz.lazy import LazyDict, LazyList, LazySet
from pytz.tzinfo import unpickler, BaseTzInfo
from pytz.tzfile import build_tzinfo
import doctest
import pytz
from pkg_resources import resource_stream


def FixedOffset(offset, _tzinfos={}):
    "return a fixed-offset timezone based off a number of minutes.\n\n        >>> one = FixedOffset(-330)\n        >>> one\n        pytz.FixedOffset(-330)\n        >>> str(one.utcoffset(datetime.datetime.now()))\n        '-1 day, 18:30:00'\n        >>> str(one.dst(datetime.datetime.now()))\n        '0:00:00'\n\n        >>> two = FixedOffset(1380)\n        >>> two\n        pytz.FixedOffset(1380)\n        >>> str(two.utcoffset(datetime.datetime.now()))\n        '23:00:00'\n        >>> str(two.dst(datetime.datetime.now()))\n        '0:00:00'\n\n    The datetime.timedelta must be between the range of -1 and 1 day,\n    non-inclusive.\n\n        >>> FixedOffset(1440)\n        Traceback (most recent call last):\n        ...\n        ValueError: ('absolute offset is too large', 1440)\n\n        >>> FixedOffset(-1440)\n        Traceback (most recent call last):\n        ...\n        ValueError: ('absolute offset is too large', -1440)\n\n    An offset of 0 is special-cased to return UTC.\n\n        >>> FixedOffset(0) is UTC\n        True\n\n    There should always be only one instance of a FixedOffset per timedelta.\n    This should be true for multiple creation calls.\n\n        >>> FixedOffset(-330) is one\n        True\n        >>> FixedOffset(1380) is two\n        True\n\n    It should also be true for pickling.\n\n        >>> import pickle\n        >>> pickle.loads(pickle.dumps(one)) is one\n        True\n        >>> pickle.loads(pickle.dumps(two)) is two\n        True\n    "
    if (offset == 0):
        return UTC
    info = _tzinfos.get(offset)
    if (info is None):
        info = _tzinfos.setdefault(offset, _FixedOffset(offset))
    return info
