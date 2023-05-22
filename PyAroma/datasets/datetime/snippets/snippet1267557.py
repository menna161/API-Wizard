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


def normalize(self, dt, is_dst=False):
    'Correct the timezone information on the given datetime'
    if (dt.tzinfo is self):
        return dt
    if (dt.tzinfo is None):
        raise ValueError('Naive time - no tzinfo set')
    return dt.astimezone(self)
