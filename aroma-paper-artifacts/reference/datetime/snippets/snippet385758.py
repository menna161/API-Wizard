import threading
from abc import ABCMeta, abstractmethod
from copy import deepcopy
from datetime import datetime, timedelta
from random import randint
from .lru import LRUCache


def __refresh(self):
    'Refresh the cached object when needed.\n\n        :rtype: None\n        :return: None\n        '
    if (not self._is_refresh_needed()):
        return
    self._refresh_needed = False
    try:
        self._set_result(self._execute_refresh())
        self._exception = None
        self._exception_count = 0
    except Exception as e:
        self._exception = e
        delay = (self._config.exception_retry_delay_base * (self._config.exception_retry_growth_factor ** self._exception_count))
        self._exception_count += 1
        delay = min(delay, self._config.exception_retry_delay_max)
        self._next_retry_time = (datetime.utcnow() + timedelta(milliseconds=delay))
