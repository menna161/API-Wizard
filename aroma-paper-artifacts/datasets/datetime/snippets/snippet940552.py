import types
import typing as T
import collections
import datetime
import re
import voluptuous as vol


def build_date_from_constraint(constraint: T.Dict[(str, int)], default_date: datetime.date, direction: int=0) -> datetime.date:
    'Builds and returns a datetime.date object from the given constraint,\n    taking missing values from the given default_date.\n    In case the date is not valid (e.g. 2017-02-29), a ValueError is\n    raised, unless a number has been given for direction, in which case\n    the next/previous valid date will be chosen, depending on the sign\n    of direction.'
    fields = {}
    for field in ('year', 'month', 'day'):
        fields[field] = constraint.get(field, getattr(default_date, field))
    while True:
        try:
            return datetime.date(**fields)
        except ValueError:
            if (direction > 0):
                fields['day'] += 1
            elif (direction < 0):
                fields['day'] -= 1
            else:
                raise
            if (fields['day'] < 1):
                fields['day'] = 31
                fields['month'] -= 1
            elif (fields['day'] > 31):
                fields['day'] = 1
                fields['month'] += 1
            if (fields['month'] < 1):
                fields['month'] = 12
                fields['year'] -= 1
            elif (fields['month'] > 12):
                fields['month'] = 1
                fields['year'] += 1
