from __future__ import division
from datetime import datetime
from pip._vendor.cachecontrol.cache import BaseCache


def set(self, key, value, expires=None):
    if (not expires):
        self.conn.set(key, value)
    else:
        expires = (expires - datetime.utcnow())
        self.conn.setex(key, int(expires.total_seconds()), value)
