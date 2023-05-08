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


def set(self, url, content):
    f = LockedFile(self._file, 'r+', 'r')
    try:
        f.open_and_lock()
        if f.is_locked():
            cache = _read_or_initialize_cache(f)
            cache[url] = (content, _to_timestamp(datetime.datetime.now()))
            for (k, (_, timestamp)) in list(cache.items()):
                if (_to_timestamp(datetime.datetime.now()) >= (timestamp + self._max_age)):
                    del cache[k]
            f.file_handle().truncate(0)
            f.file_handle().seek(0)
            json.dump(cache, f.file_handle())
        else:
            LOGGER.debug('Could not obtain a lock for the cache file.')
    except Exception as e:
        LOGGER.warning(e, exc_info=True)
    finally:
        f.unlock_and_close()
