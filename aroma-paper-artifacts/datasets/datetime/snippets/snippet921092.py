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


@reify
def if_range(self) -> Optional[datetime.datetime]:
    'The value of If-Range HTTP header, or None.\n\n        This header is represented as a `datetime` object.\n        '
    return self._http_date(self.headers.get(hdrs.IF_RANGE))
