import typing as T
import datetime
import functools
from cached_property import cached_property
from . import util
from . import expression
import types
from .room import Room


@staticmethod
def _format_time(_time: datetime.time=None, days: int=None) -> str:
    'Formats time + shift days as a string for use in __repr__.'
    if (_time is None):
        time_repr = '??:??'
    else:
        time_repr = _time.strftime(('%H:%M:%S' if _time.second else '%H:%M'))
    if (days is None):
        days_repr = ''
    elif (days < 0):
        days_repr = '{}d'.format(days)
    else:
        days_repr = '+{}d'.format(days)
    return '{}{}'.format(time_repr, days_repr)
