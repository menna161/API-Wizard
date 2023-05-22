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


def localize(self, dt, is_dst=False):
    'Convert naive time to local time'
    if (dt.tzinfo is not None):
        raise ValueError('Not naive datetime (tzinfo is already set)')
    return dt.replace(tzinfo=self)
