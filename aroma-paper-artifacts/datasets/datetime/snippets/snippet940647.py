import typing as T
import datetime
import inspect
import itertools
from .. import schedule as schedule_mod
from ..room import Room


def evaluate(self, schedule: 'schedule_mod.Schedule', when: datetime.datetime=None) -> T.Any:
    'Evaluates the given schedule for the given point in time.'
    when = (when or self._now)
    return schedule.evaluate(self._room, when)
