from base64 import b64decode, b64encode
from datetime import datetime, timezone
from email import utils
from re import findall, fullmatch
from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import quote as url_quote, unquote as url_unquote
from kiss_headers.models import Header
from kiss_headers.utils import class_to_header_name, header_content_split, prettify_header_name, quote, unquote


def __init__(self, auth_type: Optional[str]=None, challenge: str='realm', value: str='Secured area', **kwargs: Optional[str]):
    '\n        >>> www_authenticate = WwwAuthenticate("Basic", "realm", "Secured area")\n        >>> repr(www_authenticate)\n        \'Www-Authenticate: Basic realm="Secured area"\'\n        >>> headers = www_authenticate + WwwAuthenticate(challenge="charset", value="UTF-8")\n        >>> repr(headers)\n        \'Www-Authenticate: Basic realm="Secured area", charset="UTF-8"\'\n        >>> www_authenticate.get_challenge()\n        (\'realm\', \'Secured area\')\n        >>> www_authenticate.get_auth_type()\n        \'Basic\'\n        '
    super().__init__(f"""{((auth_type + ' ') if auth_type else '')}{challenge}="{value}"""", **kwargs)
