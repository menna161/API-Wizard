import typing as T
import datetime
import functools
from cached_property import cached_property
from . import util
from . import expression
import types
from .room import Room


def check_constraints(self, date: datetime.date) -> bool:
    'Checks constraints of all rules along this path against the\n        given date and returns whether they are all fulfilled.'
    for rule in self.rules:
        if (not rule.check_constraints(date)):
            return False
    return True
