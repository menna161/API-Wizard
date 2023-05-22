from __future__ import absolute_import, division, print_function, unicode_literals
import datetime
import importlib
import inspect
import re
import trafaret as t
from croniter import croniter
from trafaret import Any, Bool, Dict, Email, Enum, Int, Key, List, Mapping, Null, String
from inspect import signature
from funcsigs import signature


def cast_interval(value):
    'Casts interval value into `datetime.timedelta` instance.\n\n    If value is `int`, returned `timedelta` get constructed from a given\n    by the value`s seconds.\n\n    If value is `str`, then it get converted into seconds according the rules:\n\n    - ``\\d+s`` - time delta in seconds. Example: ``10s`` for 10 seconds;\n    - ``\\d+m`` - time delta in minutes. Example: ``42m`` for 42 minutes;\n    - ``\\d+h`` - time delta in hours. Example: ``1h`` for 1 hour;\n    - ``\\d+d`` - time delta in days. Example: ``10d`` for 10 days.\n\n    :param str | int | datetime.timedelta value: An interval value.\n    :rtype: datetime.timedelta\n    '
    if isinstance(value, str):
        match = re.match('^(-)?(\\d+)([dhms])$', value)
        if (match is not None):
            (has_neg_sign, value, unit) = match.groups()
            value = int(value)
            value *= {'s': 1, 'm': 60, 'h': (60 * 60), 'd': ((60 * 60) * 24)}[unit]
            value *= ((- 1) if has_neg_sign else 1)
    if isinstance(value, int):
        value = datetime.timedelta(seconds=value)
    elif (not isinstance(value, datetime.timedelta)):
        raise t.DataError(('invalid interval value %s' % value))
    return value
