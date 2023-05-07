import time
from collections import namedtuple
from datetime import datetime, timedelta
from requests import Session
from requests.exceptions import ConnectionError
from .exceptions import HTTP_EXCEPTIONS, TransportError


def get_backoff_timedelta(self):
    if (self.backoff_time is None):
        return 0
    return (self.backoff_time - datetime.utcnow()).total_seconds()
