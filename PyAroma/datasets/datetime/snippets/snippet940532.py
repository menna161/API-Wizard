import typing as T
import datetime
import functools
from cached_property import cached_property
from . import util
from . import expression
import types
from .room import Room


def map_func(_time: datetime.time) -> datetime.datetime:
    'Maps a time object to a datetime containing the next\n            occurrence of that time. Midnight transitions are handled\n            correctly.'
    if (_time <= current_time):
        return datetime.datetime.combine(tomorrow, _time)
    return datetime.datetime.combine(today, _time)
