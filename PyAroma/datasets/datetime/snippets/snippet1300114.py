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


def _parse_datetime(self, value: str) -> datetime.datetime:
    for format in self._DATETIME_FORMATS:
        try:
            return datetime.datetime.strptime(value, format)
        except ValueError:
            pass
    raise Error(('Unrecognized date/time format: %r' % value))
