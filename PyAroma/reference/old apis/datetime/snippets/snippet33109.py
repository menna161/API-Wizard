import os
from collections import Mapping
from datetime import datetime
from .auth import _basic_auth_str
from .compat import cookielib, OrderedDict, urljoin, urlparse
from .cookies import cookiejar_from_dict, extract_cookies_to_jar, RequestsCookieJar, merge_cookies
from .models import Request, PreparedRequest, DEFAULT_REDIRECT_LIMIT
from .hooks import default_hooks, dispatch_hook
from .utils import to_key_val_list, default_headers, to_native_string
from .exceptions import TooManyRedirects, InvalidSchema, ChunkedEncodingError, ContentDecodingError
from .packages.urllib3._collections import RecentlyUsedContainer
from .structures import CaseInsensitiveDict
from .adapters import HTTPAdapter
from .utils import requote_uri, get_environ_proxies, get_netrc_auth, should_bypass_proxies, get_auth_from_url
from .status_codes import codes
from .models import REDIRECT_STATI


def send(self, request, **kwargs):
    'Send a given PreparedRequest.'
    kwargs.setdefault('stream', self.stream)
    kwargs.setdefault('verify', self.verify)
    kwargs.setdefault('cert', self.cert)
    kwargs.setdefault('proxies', self.proxies)
    if isinstance(request, Request):
        raise ValueError('You can only send PreparedRequests.')
    allow_redirects = kwargs.pop('allow_redirects', True)
    stream = kwargs.get('stream')
    hooks = request.hooks
    if allow_redirects:
        checked_urls = set()
        while (request.url in self.redirect_cache):
            checked_urls.add(request.url)
            new_url = self.redirect_cache.get(request.url)
            if (new_url in checked_urls):
                break
            request.url = new_url
    adapter = self.get_adapter(url=request.url)
    start = datetime.utcnow()
    r = adapter.send(request, **kwargs)
    r.elapsed = (datetime.utcnow() - start)
    r = dispatch_hook('response', hooks, r, **kwargs)
    if r.history:
        for resp in r.history:
            extract_cookies_to_jar(self.cookies, resp.request, resp.raw)
    extract_cookies_to_jar(self.cookies, request, r.raw)
    gen = self.resolve_redirects(r, request, **kwargs)
    history = ([resp for resp in gen] if allow_redirects else [])
    if history:
        history.insert(0, r)
        r = history.pop()
        r.history = history
    if (not stream):
        r.content
    return r
