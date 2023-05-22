import typing as T
import datetime
import functools
from cached_property import cached_property
from . import util
from . import expression
import types
from .room import Room


def get_next_scheduling_datetime(self, now: datetime.datetime) -> T.Optional[datetime.datetime]:
    'Returns a datetime object with the time at which the next\n        re-scheduling should be done. now should be a datetime object\n        containing the current date and time.\n        SubScheduleRule objects and their rules are considered as well.\n        None is returned in case there are no rules in the schedule.'
    times = self.get_scheduling_times()
    if (not times):
        return None
    current_time = now.time()
    today = now.date()
    tomorrow = (today + datetime.timedelta(days=1))

    def map_func(_time: datetime.time) -> datetime.datetime:
        'Maps a time object to a datetime containing the next\n            occurrence of that time. Midnight transitions are handled\n            correctly.'
        if (_time <= current_time):
            return datetime.datetime.combine(tomorrow, _time)
        return datetime.datetime.combine(today, _time)
    return min(map(map_func, times))
