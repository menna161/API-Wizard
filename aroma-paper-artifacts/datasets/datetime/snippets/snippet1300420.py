import base64
import binascii
import datetime
import email.utils
import functools
import gzip
import hashlib
import hmac
import http.cookies
from inspect import isclass
from io import BytesIO
import mimetypes
import numbers
import os.path
import re
import sys
import threading
import time
import tornado
import traceback
import types
import urllib.parse
from urllib.parse import urlencode
from tornado.concurrent import Future, future_set_result_unless_cancelled
from tornado import escape
from tornado import gen
from tornado.httpserver import HTTPServer
from tornado import httputil
from tornado import iostream
import tornado.locale
from tornado import locale
from tornado.log import access_log, app_log, gen_log
from tornado import template
from tornado.escape import utf8, _unicode
from tornado.routing import AnyMatches, DefaultHostMatches, HostMatches, ReversibleRouter, Rule, ReversibleRuleRouter, URLSpec, _RuleList
from tornado.util import ObjectDict, unicode_type, _websocket_mask
from typing import Dict, Any, Union, Optional, Awaitable, Tuple, List, Callable, Iterable, Generator, Type, cast, overload
from types import TracebackType
import typing
from typing import Set
from tornado import autoreload


def _convert_header_value(self, value: _HeaderTypes) -> str:
    if isinstance(value, str):
        retval = value
    elif isinstance(value, bytes):
        retval = value.decode('latin1')
    elif isinstance(value, unicode_type):
        retval = escape.utf8(value)
    elif isinstance(value, numbers.Integral):
        return str(value)
    elif isinstance(value, datetime.datetime):
        return httputil.format_timestamp(value)
    else:
        raise TypeError(('Unsupported header value %r' % value))
    if RequestHandler._INVALID_HEADER_CHAR_RE.search(retval):
        raise ValueError('Unsafe header value %r', retval)
    return retval
