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


def check_and_return(self, value):
    if isinstance(value, datetime.datetime):
        return value
    if (not isinstance(value, datetime.date)):
        self._failure('value should be a date', value=value)
    time = datetime.datetime.min.time()
    return datetime.datetime.combine(value, time)
