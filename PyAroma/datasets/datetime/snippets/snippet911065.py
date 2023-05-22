import logging
import os
from collections import OrderedDict
from datetime import datetime
from threading import Lock
from .defaults import LEVEL_MAP
from .exceptions import ConfigurationWarning


def filter(self, record):
    msg = record.getMessage()
    with self.lock:
        if (msg in self._cache):
            now = datetime.utcnow()
            delta = (now - self._cache[msg]['time'])
            if (delta.seconds >= self._cache_expire):
                self._cache[msg]['time'] = now
                self._cache[msg]['hits'] = 10
                return True
            self._cache[msg]['hits'] += 1
            return False
    if (len(self._cache) >= self._cache_size):
        with self.lock:
            (key, _) = sorted(self._cache.items(), key=(lambda t: t[1]['hits']))[0]
            self._cache.pop(key, None)
    with self.lock:
        self._cache[msg] = {'time': datetime.utcnow(), 'hits': 0}
    return True
