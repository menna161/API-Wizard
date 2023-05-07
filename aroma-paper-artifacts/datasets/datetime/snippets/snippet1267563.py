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


def __init__(self, minutes):
    if (abs(minutes) >= 1440):
        raise ValueError('absolute offset is too large', minutes)
    self._minutes = minutes
    self._offset = datetime.timedelta(minutes=minutes)
