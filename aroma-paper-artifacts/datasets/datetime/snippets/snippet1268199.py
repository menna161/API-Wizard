import datetime
import sys
import encodings.idna
from urllib3.fields import RequestField
from urllib3.filepost import encode_multipart_formdata
from urllib3.util import parse_url
from urllib3.exceptions import DecodeError, ReadTimeoutError, ProtocolError, LocationParseError
from io import UnsupportedOperation
from .hooks import default_hooks
from .structures import CaseInsensitiveDict
from .auth import HTTPBasicAuth
from .cookies import cookiejar_from_dict, get_cookie_header, _copy_cookie_jar
from .exceptions import HTTPError, MissingSchema, InvalidURL, ChunkedEncodingError, ContentDecodingError, ConnectionError, StreamConsumedError
from ._internal_utils import to_native_string, unicode_is_ascii
from .utils import guess_filename, get_auth_from_url, requote_uri, stream_decode_response_unicode, to_key_val_list, parse_header_links, iter_slices, guess_json_utf, super_len, check_header_validity
from .compat import Callable, Mapping, cookielib, urlunparse, urlsplit, urlencode, str, bytes, is_py2, chardet, builtin_str, basestring
from .compat import json as complexjson
from .status_codes import codes
import idna


def __init__(self):
    self._content = False
    self._content_consumed = False
    self._next = None
    self.status_code = None
    self.headers = CaseInsensitiveDict()
    self.raw = None
    self.url = None
    self.encoding = None
    self.history = []
    self.reason = None
    self.cookies = cookiejar_from_dict({})
    self.elapsed = datetime.timedelta(0)
    self.request = None
