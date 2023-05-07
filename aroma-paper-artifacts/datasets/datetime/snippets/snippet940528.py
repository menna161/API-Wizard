import typing as T
import datetime
import functools
from cached_property import cached_property
from . import util
from . import expression
import types
from .room import Room


def get_scheduling_times(self) -> T.Set[datetime.time]:
    'Returns a set of times a re-scheduling should be triggered\n        at. Rules of sub-schedules are considered as well.'
    times = set()
    for path in self.unfolded:
        if (not path.is_always_active):
            (start_time, _, end_time, _) = path.times
            times.update((start_time, end_time))
    return times
