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


def get_cache_time(self, path: str, modified: Optional[datetime.datetime], mime_type: str) -> int:
    'Override to customize cache control behavior.\n\n        Return a positive number of seconds to make the result\n        cacheable for that amount of time or 0 to mark resource as\n        cacheable for an unspecified amount of time (subject to\n        browser heuristics).\n\n        By default returns cache expiry of 10 years for resources requested\n        with ``v`` argument.\n        '
    return (self.CACHE_MAX_AGE if ('v' in self.request.arguments) else 0)
