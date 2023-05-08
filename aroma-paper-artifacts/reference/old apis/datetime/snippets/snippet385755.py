import threading
from abc import ABCMeta, abstractmethod
from copy import deepcopy
from datetime import datetime, timedelta
from random import randint
from .lru import LRUCache


def _is_refresh_needed(self):
    'Determine if the cached object should be refreshed.\n\n        :rtype: bool\n        :return: True if the object should be refreshed.\n        '
    if self._refresh_needed:
        return True
    if (self._exception is None):
        return False
    if (self._next_retry_time is None):
        return False
    return (self._next_retry_time <= datetime.utcnow())
