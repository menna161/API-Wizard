import collections
import datetime
from io import BytesIO, UnsupportedOperation
from .hooks import default_hooks
from .structures import CaseInsensitiveDict
from .auth import HTTPBasicAuth
from .cookies import cookiejar_from_dict, get_cookie_header
from .packages.urllib3.fields import RequestField
from .packages.urllib3.filepost import encode_multipart_formdata
from .packages.urllib3.util import parse_url
from .packages.urllib3.exceptions import DecodeError, ReadTimeoutError, ProtocolError, LocationParseError
from .exceptions import HTTPError, MissingSchema, InvalidURL, ChunkedEncodingError, ContentDecodingError, ConnectionError, StreamConsumedError
from .utils import guess_filename, get_auth_from_url, requote_uri, stream_decode_response_unicode, to_key_val_list, parse_header_links, iter_slices, guess_json_utf, super_len, to_native_string
from .compat import cookielib, urlunparse, urlsplit, urlencode, str, bytes, StringIO, is_py2, chardet, json, builtin_str, basestring
from .status_codes import codes


def __init__(self):
    super(Response, self).__init__()
    self._content = False
    self._content_consumed = False
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
