import typing as T
import datetime
import inspect
import itertools
from .. import schedule as schedule_mod
from ..room import Room


def next_results(self, schedule: 'schedule_mod.Schedule', start: datetime.datetime=None, end: datetime.datetime=None) -> T.Generator[(T.Tuple[(datetime.datetime, 'schedule_mod.ScheduleEvaluationResultType')], None, None)]:
    'Returns a generator that yields tuples of datetime objects\n        and schedule evaluation results. At each of these datetimes,\n        the scheduling result will change to the returned one.\n        The first result generated is always that for the start time,\n        the last one that for the end time.'
    when = (start or self._now)
    last_result = None
    while (when and ((not end) or (end > when))):
        result = schedule.evaluate(self._room, when)
        if (result and (result != last_result)):
            (yield (when, result))
            last_result = result
        when = schedule.get_next_scheduling_datetime(when)
    if (end and last_result):
        (yield (end, last_result))
