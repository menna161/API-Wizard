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


def should_return_304(self) -> bool:
    'Returns True if the headers indicate that we should return 304.\n\n        .. versionadded:: 3.1\n        '
    if self.request.headers.get('If-None-Match'):
        return self.check_etag_header()
    ims_value = self.request.headers.get('If-Modified-Since')
    if (ims_value is not None):
        date_tuple = email.utils.parsedate(ims_value)
        if (date_tuple is not None):
            if_since = datetime.datetime(*date_tuple[:6])
            assert (self.modified is not None)
            if (if_since >= self.modified):
                return True
    return False
