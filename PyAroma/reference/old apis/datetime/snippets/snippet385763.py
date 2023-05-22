import threading
from abc import ABCMeta, abstractmethod
from copy import deepcopy
from datetime import datetime, timedelta
from random import randint
from .lru import LRUCache


def _is_refresh_needed(self):
    'Determine if the cached item should be refreshed.\n\n        :rtype: bool\n        :return: True if a refresh is needed.\n        '
    if super(SecretCacheItem, self)._is_refresh_needed():
        return True
    if self._exception:
        return False
    return (self._next_refresh_time <= datetime.utcnow())
