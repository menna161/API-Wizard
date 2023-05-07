import typing as T
import datetime
import functools
from cached_property import cached_property
from . import util
from . import expression
import types
from .room import Room


def is_active(self, when: datetime.datetime) -> bool:
    'Returns whether the rule this path leads to is active at\n        given point in time.'
    if self.is_always_active:
        return True
    (_date, _time) = (when.date(), when.time())
    (start_time, start_plus_days, end_time, end_plus_days) = self.times
    shift_list = list(range((end_plus_days + 1)))
    if (_time >= end_time):
        del shift_list[(- 1)]
    if (shift_list and (_time < start_time)):
        del shift_list[0]
    for days_back in shift_list:
        start_date = (_date - datetime.timedelta(days=(days_back + start_plus_days)))
        if (not self.check_constraints(start_date)):
            continue
        return True
    return False
