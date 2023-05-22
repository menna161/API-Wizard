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


def _expire_cookie(self, when: datetime.datetime, domain: str, name: str) -> None:
    self._next_expiration = min(self._next_expiration, when)
    self._expirations[(domain, name)] = when
