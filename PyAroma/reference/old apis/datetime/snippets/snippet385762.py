import threading
from abc import ABCMeta, abstractmethod
from copy import deepcopy
from datetime import datetime, timedelta
from random import randint
from .lru import LRUCache


def __init__(self, config, client, secret_id):
    "Construct a secret cache item.\n\n\n        :type config: aws_secretsmanager_caching.SecretCacheConfig\n        :param config: Configuration for the cache.\n\n        :type client: botocore.client.BaseClient\n        :param client: The 'secretsmanager' boto client.\n\n        :type secret_id: str\n        :param secret_id: The secret identifier to cache.\n        "
    super(SecretCacheItem, self).__init__(config, client, secret_id)
    self._versions = LRUCache(10)
    self._next_refresh_time = datetime.utcnow()
