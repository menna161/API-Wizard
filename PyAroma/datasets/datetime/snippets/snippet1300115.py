import datetime
import numbers
import re
import sys
import os
import textwrap
from tornado.escape import _unicode, native_str
from tornado.log import define_logging_options
from tornado.util import basestring_type, exec_in
import typing
from typing import Any, Iterator, Iterable, Tuple, Set, Dict, Callable, List, TextIO
from typing import Optional


def _parse_timedelta(self, value: str) -> datetime.timedelta:
    try:
        sum = datetime.timedelta()
        start = 0
        while (start < len(value)):
            m = self._TIMEDELTA_PATTERN.match(value, start)
            if (not m):
                raise Exception()
            num = float(m.group(1))
            units = (m.group(2) or 'seconds')
            units = self._TIMEDELTA_ABBREV_DICT.get(units, units)
            sum += datetime.timedelta(**{units: num})
            start = m.end()
        return sum
    except Exception:
        raise
