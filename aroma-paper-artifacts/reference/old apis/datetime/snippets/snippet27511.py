import datetime
import encodings.idna
from io import UnsupportedOperation
from urllib3.exceptions import DecodeError, LocationParseError, ProtocolError, ReadTimeoutError, SSLError
from urllib3.fields import RequestField
from urllib3.filepost import encode_multipart_formdata
from urllib3.util import parse_url
from ._internal_utils import to_native_string, unicode_is_ascii
from .auth import HTTPBasicAuth
from .compat import Callable, JSONDecodeError, Mapping, basestring, builtin_str, chardet, cookielib
from .compat import json as complexjson
from .compat import urlencode, urlsplit, urlunparse
from .cookies import _copy_cookie_jar, cookiejar_from_dict, get_cookie_header
from .exceptions import ChunkedEncodingError, ConnectionError, ContentDecodingError, HTTPError, InvalidJSONError, InvalidURL
from .exceptions import JSONDecodeError as RequestsJSONDecodeError
from .exceptions import MissingSchema
from .exceptions import SSLError as RequestsSSLError
from .exceptions import StreamConsumedError
from .hooks import default_hooks
from .status_codes import codes
from .structures import CaseInsensitiveDict
from .utils import check_header_validity, get_auth_from_url, guess_filename, guess_json_utf, iter_slices, parse_header_links, requote_uri, stream_decode_response_unicode, super_len, to_key_val_list
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
