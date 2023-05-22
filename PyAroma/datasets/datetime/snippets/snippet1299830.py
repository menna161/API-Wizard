import calendar
import collections
import copy
import datetime
import email.utils
from http.client import responses
import http.cookies
import re
from ssl import SSLError
import time
import unicodedata
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl
from tornado.escape import native_str, parse_qs_bytes, utf8
from tornado.log import gen_log
from tornado.util import ObjectDict, unicode_type
import typing
from typing import Tuple, Iterable, List, Mapping, Iterator, Dict, Union, Optional, Awaitable, Generator, AnyStr
from typing import Deque
from asyncio import Future
import unittest
import doctest


def format_timestamp(ts: Union[(int, float, tuple, time.struct_time, datetime.datetime)]) -> str:
    "Formats a timestamp in the format used by HTTP.\n\n    The argument may be a numeric timestamp as returned by `time.time`,\n    a time tuple as returned by `time.gmtime`, or a `datetime.datetime`\n    object.\n\n    >>> format_timestamp(1359312200)\n    'Sun, 27 Jan 2013 18:43:20 GMT'\n    "
    if isinstance(ts, (int, float)):
        time_num = ts
    elif isinstance(ts, (tuple, time.struct_time)):
        time_num = calendar.timegm(ts)
    elif isinstance(ts, datetime.datetime):
        time_num = calendar.timegm(ts.utctimetuple())
    else:
        raise TypeError(('unknown timestamp type: %r' % ts))
    return email.utils.formatdate(time_num, usegmt=True)
