import asyncio
import datetime
import os
import pathlib
import pickle
import re
from collections import defaultdict
from http.cookies import BaseCookie, Morsel, SimpleCookie
from typing import DefaultDict, Dict, Iterable, Iterator, Mapping, Optional, Set, Tuple, Union, cast
from yarl import URL
from .abc import AbstractCookieJar
from .helpers import is_ip_address, next_whole_second
from .typedefs import LooseCookies, PathLike


def update_cookies(self, cookies: LooseCookies, response_url: URL=URL()) -> None:
    'Update cookies.'
    hostname = response_url.raw_host
    if ((not self._unsafe) and is_ip_address(hostname)):
        return
    if isinstance(cookies, Mapping):
        cookies = cookies.items()
    for (name, cookie) in cookies:
        if (not isinstance(cookie, Morsel)):
            tmp = SimpleCookie()
            tmp[name] = cookie
            cookie = tmp[name]
        domain = cookie['domain']
        if domain.endswith('.'):
            domain = ''
            del cookie['domain']
        if ((not domain) and (hostname is not None)):
            self._host_only_cookies.add((hostname, name))
            domain = cookie['domain'] = hostname
        if domain.startswith('.'):
            domain = domain[1:]
            cookie['domain'] = domain
        if (hostname and (not self._is_domain_match(domain, hostname))):
            continue
        path = cookie['path']
        if ((not path) or (not path.startswith('/'))):
            path = response_url.path
            if (not path.startswith('/')):
                path = '/'
            else:
                path = ('/' + path[1:path.rfind('/')])
            cookie['path'] = path
        max_age = cookie['max-age']
        if max_age:
            try:
                delta_seconds = int(max_age)
                try:
                    max_age_expiration = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=delta_seconds))
                except OverflowError:
                    max_age_expiration = self.MAX_TIME
                self._expire_cookie(max_age_expiration, domain, name)
            except ValueError:
                cookie['max-age'] = ''
        else:
            expires = cookie['expires']
            if expires:
                expire_time = self._parse_date(expires)
                if expire_time:
                    self._expire_cookie(expire_time, domain, name)
                else:
                    cookie['expires'] = ''
        self._cookies[domain][name] = cookie
    self._do_expiration()
