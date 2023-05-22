import asyncio
import datetime
import io
import re
import socket
import string
import tempfile
import types
import warnings
from email.utils import parsedate
from http.cookies import SimpleCookie
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Dict, Iterator, Mapping, MutableMapping, Optional, Tuple, Union, cast
from urllib.parse import parse_qsl
import attr
from multidict import CIMultiDict, CIMultiDictProxy, MultiDict, MultiDictProxy
from yarl import URL
from . import hdrs
from .abc import AbstractStreamWriter
from .helpers import DEBUG, ChainMapProxy, HeadersMixin, reify, sentinel
from .http_parser import RawRequestMessage
from .multipart import BodyPartReader, MultipartReader
from .streams import EmptyStreamReader, StreamReader
from .typedefs import DEFAULT_JSON_DECODER, JSONDecoder, LooseHeaders, RawHeaders, StrOrURL
from .web_exceptions import HTTPRequestEntityTooLarge
from .web_response import StreamResponse
from .web_app import Application
from .web_urldispatcher import UrlMappingMatchInfo
from .web_protocol import RequestHandler


@staticmethod
def _http_date(_date_str: str) -> Optional[datetime.datetime]:
    'Process a date string, return a datetime object\n        '
    if (_date_str is not None):
        timetuple = parsedate(_date_str)
        if (timetuple is not None):
            return datetime.datetime(*timetuple[:6], tzinfo=datetime.timezone.utc)
    return None
