import threading
from abc import ABCMeta, abstractmethod
from copy import deepcopy
from datetime import datetime, timedelta
from random import randint
from .lru import LRUCache


def _execute_refresh(self):
    'Perform the actual refresh of the cached secret information.\n\n        :rtype: dict\n        :return: The result of the DescribeSecret request.\n        '
    result = self._client.describe_secret(SecretId=self._secret_id)
    ttl = self._config.secret_refresh_interval
    self._next_refresh_time = (datetime.utcnow() + timedelta(seconds=randint(round((ttl / 2)), ttl)))
    return result
