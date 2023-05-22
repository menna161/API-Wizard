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


def set_cookie(self, name: str, value: Union[(str, bytes)], domain: str=None, expires: Union[(float, Tuple, datetime.datetime)]=None, path: str='/', expires_days: int=None, **kwargs: Any) -> None:
    'Sets an outgoing cookie name/value with the given options.\n\n        Newly-set cookies are not immediately visible via `get_cookie`;\n        they are not present until the next request.\n\n        expires may be a numeric timestamp as returned by `time.time`,\n        a time tuple as returned by `time.gmtime`, or a\n        `datetime.datetime` object.\n\n        Additional keyword arguments are set on the cookies.Morsel\n        directly.\n        See https://docs.python.org/3/library/http.cookies.html#http.cookies.Morsel\n        for available attributes.\n        '
    name = escape.native_str(name)
    value = escape.native_str(value)
    if re.search('[\\x00-\\x20]', (name + value)):
        raise ValueError(('Invalid cookie %r: %r' % (name, value)))
    if (not hasattr(self, '_new_cookie')):
        self._new_cookie = http.cookies.SimpleCookie()
    if (name in self._new_cookie):
        del self._new_cookie[name]
    self._new_cookie[name] = value
    morsel = self._new_cookie[name]
    if domain:
        morsel['domain'] = domain
    if ((expires_days is not None) and (not expires)):
        expires = (datetime.datetime.utcnow() + datetime.timedelta(days=expires_days))
    if expires:
        morsel['expires'] = httputil.format_timestamp(expires)
    if path:
        morsel['path'] = path
    for (k, v) in kwargs.items():
        if (k == 'max_age'):
            k = 'max-age'
        if ((k in ['httponly', 'secure']) and (not v)):
            continue
        morsel[k] = v
