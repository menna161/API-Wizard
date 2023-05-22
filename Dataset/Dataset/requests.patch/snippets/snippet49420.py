from typing import Optional, Any, Iterator
from timeit import default_timer as timer
import contextlib
import logging
import time
import requests
import urllib3.exceptions
import urllib.parse
from ..exceptions import ConnectionFailure, UnexpectedResponse, BugZooException
from typing import NoReturn
from mypy_extensions import NoReturn


@contextlib.contextmanager
def patch(self, path: str, data, **kwargs) -> Iterator[requests.Response]:
    url = self._url(path)
    logger.debug('PATCH: %s', url)
    with contextlib.closing(requests.patch(url, data=data, **kwargs)) as r:
        (yield r)
