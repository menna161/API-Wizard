import typing as T
import datetime
import functools
from cached_property import cached_property
from . import util
from . import expression
import types
from .room import Room


def _check_constraints(self, date: datetime.date) -> bool:
    'Checks all constraints of this rule against the given date\n        and returns whether they are fulfilled'
    if (not self.constraints):
        return True
    (year, week, weekday) = date.isocalendar()
    checks = {'years': (lambda a: (year in a)), 'months': (lambda a: (date.month in a)), 'days': (lambda a: (date.day in a)), 'weeks': (lambda a: (week in a)), 'weekdays': (lambda a: (weekday in a)), 'start_date': (lambda a: (date >= util.build_date_from_constraint(a, date, 1))), 'end_date': (lambda a: (date <= util.build_date_from_constraint(a, date, (- 1))))}
    for (constraint, allowed) in self.constraints.items():
        if (not checks[constraint](allowed)):
            return False
    return True
