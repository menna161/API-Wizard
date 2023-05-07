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


def clear_cookie(self, name: str, path: str='/', domain: str=None) -> None:
    'Deletes the cookie with the given name.\n\n        Due to limitations of the cookie protocol, you must pass the same\n        path and domain to clear a cookie as were used when that cookie\n        was set (but there is no way to find out on the server side\n        which values were used for a given cookie).\n\n        Similar to `set_cookie`, the effect of this method will not be\n        seen until the following request.\n        '
    expires = (datetime.datetime.utcnow() - datetime.timedelta(days=365))
    self.set_cookie(name, value='', path=path, expires=expires, domain=domain)
