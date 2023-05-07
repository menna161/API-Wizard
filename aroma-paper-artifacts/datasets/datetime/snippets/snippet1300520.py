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


def set_headers(self) -> None:
    'Sets the content and caching headers on the response.\n\n        .. versionadded:: 3.1\n        '
    self.set_header('Accept-Ranges', 'bytes')
    self.set_etag_header()
    if (self.modified is not None):
        self.set_header('Last-Modified', self.modified)
    content_type = self.get_content_type()
    if content_type:
        self.set_header('Content-Type', content_type)
    cache_time = self.get_cache_time(self.path, self.modified, content_type)
    if (cache_time > 0):
        self.set_header('Expires', (datetime.datetime.utcnow() + datetime.timedelta(seconds=cache_time)))
        self.set_header('Cache-Control', ('max-age=' + str(cache_time)))
    self.set_extra_headers(self.path)
