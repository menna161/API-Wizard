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


@property
def last_modified(self) -> Optional[datetime.datetime]:
    'The value of Last-Modified HTTP header, or None.\n\n        This header is represented as a `datetime` object.\n        '
    httpdate = self._headers.get(hdrs.LAST_MODIFIED)
    if (httpdate is not None):
        timetuple = parsedate(httpdate)
        if (timetuple is not None):
            return datetime.datetime(*timetuple[:6], tzinfo=datetime.timezone.utc)
    return None
