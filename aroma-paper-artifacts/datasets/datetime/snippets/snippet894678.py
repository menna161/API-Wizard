import time
from collections import namedtuple
from datetime import datetime, timedelta
from requests import Session
from requests.exceptions import ConnectionError
from .exceptions import HTTP_EXCEPTIONS, TransportError


def update_backoff_time(self, success, backoff_cap=None):
    if success:
        self._retries = 0
        self.backoff_time = None
    else:
        utcnow = datetime.utcnow()
        backoff_delta = (BACKOFF_DELAY * (2 ** self._retries))
        if (backoff_cap is not None):
            backoff_delta = min(backoff_delta, backoff_cap)
        self.backoff_time = (utcnow + timedelta(seconds=backoff_delta))
        self._retries += 1
