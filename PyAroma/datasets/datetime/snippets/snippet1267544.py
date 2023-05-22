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


def _UTC():
    "Factory function for utc unpickling.\n\n    Makes sure that unpickling a utc instance always returns the same\n    module global.\n\n    These examples belong in the UTC class above, but it is obscured; or in\n    the README.txt, but we are not depending on Python 2.4 so integrating\n    the README.txt examples with the unit tests is not trivial.\n\n    >>> import datetime, pickle\n    >>> dt = datetime.datetime(2005, 3, 1, 14, 13, 21, tzinfo=utc)\n    >>> naive = dt.replace(tzinfo=None)\n    >>> p = pickle.dumps(dt, 1)\n    >>> naive_p = pickle.dumps(naive, 1)\n    >>> len(p) - len(naive_p)\n    17\n    >>> new = pickle.loads(p)\n    >>> new == dt\n    True\n    >>> new is dt\n    False\n    >>> new.tzinfo is dt.tzinfo\n    True\n    >>> utc is UTC is timezone('UTC')\n    True\n    >>> utc is timezone('GMT')\n    False\n    "
    return utc
