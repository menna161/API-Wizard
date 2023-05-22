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


def parse(self, value: str) -> Any:
    _parse = {datetime.datetime: self._parse_datetime, datetime.timedelta: self._parse_timedelta, bool: self._parse_bool, basestring_type: self._parse_string}.get(self.type, self.type)
    if self.multiple:
        self._value = []
        for part in value.split(','):
            if issubclass(self.type, numbers.Integral):
                (lo_str, _, hi_str) = part.partition(':')
                lo = _parse(lo_str)
                hi = (_parse(hi_str) if hi_str else lo)
                self._value.extend(range(lo, (hi + 1)))
            else:
                self._value.append(_parse(part))
    else:
        self._value = _parse(value)
    if (self.callback is not None):
        self.callback(self._value)
    return self.value()
