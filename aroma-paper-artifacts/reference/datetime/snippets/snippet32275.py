from __future__ import division
import datetime
import json
import logging
import os
import tempfile
import threading
from . import base
from ..discovery_cache import DISCOVERY_DOC_MAX_AGE
from oauth2client.contrib.locked_file import LockedFile
from oauth2client.locked_file import LockedFile


def get(self, url):
    f = LockedFile(self._file, 'r+', 'r')
    try:
        f.open_and_lock()
        if f.is_locked():
            cache = _read_or_initialize_cache(f)
            if (url in cache):
                (content, t) = cache.get(url, (None, 0))
                if (_to_timestamp(datetime.datetime.now()) < (t + self._max_age)):
                    return content
            return None
        else:
            LOGGER.debug('Could not obtain a lock for the cache file.')
            return None
    except Exception as e:
        LOGGER.warning(e, exc_info=True)
    finally:
        f.unlock_and_close()
