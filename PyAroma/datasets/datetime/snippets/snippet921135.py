import asyncio
import collections.abc
import datetime
import enum
import json
import math
import time
import warnings
import zlib
from concurrent.futures import Executor
from email.utils import parsedate
from http.cookies import SimpleCookie
from typing import TYPE_CHECKING, Any, Dict, Iterator, Mapping, MutableMapping, Optional, Tuple, Union, cast
from multidict import CIMultiDict, istr
from . import hdrs, payload
from .abc import AbstractStreamWriter
from .helpers import HeadersMixin, rfc822_formatted_time, sentinel
from .http import RESPONSES, SERVER_SOFTWARE, HttpVersion10, HttpVersion11
from .payload import Payload
from .typedefs import JSONEncoder, LooseHeaders
from .web_request import BaseRequest


@last_modified.setter
def last_modified(self, value: Optional[Union[(int, float, datetime.datetime, str)]]) -> None:
    if (value is None):
        self._headers.pop(hdrs.LAST_MODIFIED, None)
    elif isinstance(value, (int, float)):
        self._headers[hdrs.LAST_MODIFIED] = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(math.ceil(value)))
    elif isinstance(value, datetime.datetime):
        self._headers[hdrs.LAST_MODIFIED] = time.strftime('%a, %d %b %Y %H:%M:%S GMT', value.utctimetuple())
    elif isinstance(value, str):
        self._headers[hdrs.LAST_MODIFIED] = value
