import typing as T
import datetime
import functools
from cached_property import cached_property
from . import util
from . import expression
import types
from .room import Room


@cached_property
def times(self) -> T.Tuple[(datetime.time, int, datetime.time, int)]:
    'Returns (start_time, start_plus_days, end_time, end_plus_days) for this\n        path. Rules are searched for these values from right to left.\n        Missing times are assumed to be midnight. If not set explicitly, end_plus_days\n        is 1 if start <= end else 0.'
    for rule in reversed(self.rules):
        if (rule.start_time is not None):
            start_time = rule.start_time
            break
    else:
        start_time = datetime.time(0, 0)
    for rule in reversed(self.rules):
        if (rule.start_plus_days is not None):
            start_plus_days = rule.start_plus_days
            break
    else:
        start_plus_days = 0
    for rule in reversed(self.rules):
        if (rule.end_time is not None):
            end_time = rule.end_time
            break
    else:
        end_time = datetime.time(0, 0)
    for rule in reversed(self.rules):
        if (rule.end_plus_days is not None):
            end_plus_days = rule.end_plus_days
            break
    else:
        end_plus_days = (1 if (start_time >= end_time) else 0)
    return (start_time, start_plus_days, end_time, end_plus_days)
