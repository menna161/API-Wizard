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


def _do_expiration(self) -> None:
    now = datetime.datetime.now(datetime.timezone.utc)
    if (self._next_expiration > now):
        return
    if (not self._expirations):
        return
    next_expiration = self.MAX_TIME
    to_del = []
    cookies = self._cookies
    expirations = self._expirations
    for ((domain, name), when) in expirations.items():
        if (when <= now):
            cookies[domain].pop(name, None)
            to_del.append((domain, name))
            self._host_only_cookies.discard((domain, name))
        else:
            next_expiration = min(next_expiration, when)
    for key in to_del:
        del expirations[key]
    try:
        self._next_expiration = (next_expiration.replace(microsecond=0) + datetime.timedelta(seconds=1))
    except OverflowError:
        self._next_expiration = self.MAX_TIME
