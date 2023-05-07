from base64 import b64decode, b64encode
from datetime import datetime, timezone
from email import utils
from re import findall, fullmatch
from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import quote as url_quote, unquote as url_unquote
from kiss_headers.models import Header
from kiss_headers.utils import class_to_header_name, header_content_split, prettify_header_name, quote, unquote


def __init__(self, cookie_name: str, cookie_value: str, expires: Optional[Union[(datetime, str)]]=None, max_age: Optional[int]=None, domain: Optional[str]=None, path: Optional[str]=None, samesite: Optional[str]=None, is_secure: bool=False, is_httponly: bool=True, **kwargs: Optional[str]):
    "\n        :param cookie_name: Can be any US-ASCII characters, except control characters, spaces, or tabs.\n        :param cookie_value: Can include any US-ASCII characters excluding control characters, Whitespace, double quotes, comma, semicolon, and backslash.\n        :param expires: The maximum lifetime of the cookie as an HTTP-date timestamp. Provided datetime will be converted automatically.\n        :param max_age: Number of seconds until the cookie expires. A zero or negative number will expire the cookie immediately. If both Expires and Max-Age are set, Max-Age has precedence.\n        :param domain: Hosts to where the cookie will be sent. If omitted, defaults to the host of the current document URL, not including subdomains.\n        :param path: A path that must exist in the requested URL, or the browser won't send the Cookie header.\n        :param samesite: Asserts that a cookie must not be sent with cross-origin requests, providing some protection against cross-site request forgery attacks.\n        :param is_secure: A secure cookie is only sent to the server when a request is made with the https: scheme.\n        :param is_httponly: Forbids JavaScript from accessing the cookie.\n        :param kwargs:\n        "
    for letter in cookie_name:
        if (letter in {'<>@,;:\\"/[]?={}'}):
            raise ValueError('The cookie name can not contains any of the following char: <>@,;:"/[]?={}')
    if (samesite and (samesite.lower() not in ['strict', 'lax', 'none'])):
        raise ValueError('Samesite attribute can only be one of the following: Strict, Lax or None.')
    args: Dict = {cookie_name: cookie_value, 'expires': (utils.format_datetime(expires.astimezone(timezone.utc), usegmt=True) if isinstance(expires, datetime) else expires), 'max-age': max_age, 'domain': domain, 'path': path, 'samesite': samesite}
    args.update(kwargs)
    super().__init__('', **args)
    if is_secure:
        self += 'Secure'
    if is_httponly:
        self += 'HttpOnly'
