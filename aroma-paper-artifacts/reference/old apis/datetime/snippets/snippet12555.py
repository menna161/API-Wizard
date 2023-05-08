import inspect
import numpy as np
import re
import os
import sys
from contextlib import contextmanager
from datetime import datetime, timedelta
from tqdm import tqdm
from . import logger
from .concurrency import subproc_call
from ctypes.util import find_library
from ipykernel import iostream


def humanize_time_delta(sec):
    'Humanize timedelta given in seconds\n\n    Args:\n        sec (float): time difference in seconds. Must be positive.\n\n    Returns:\n        str - time difference as a readable string\n\n    Example:\n\n    .. code-block:: python\n\n        print(humanize_time_delta(1))                                   # 1 second\n        print(humanize_time_delta(60 + 1))                              # 1 minute 1 second\n        print(humanize_time_delta(87.6))                                # 1 minute 27 seconds\n        print(humanize_time_delta(0.01))                                # 0.01 seconds\n        print(humanize_time_delta(60 * 60 + 1))                         # 1 hour 1 second\n        print(humanize_time_delta(60 * 60 * 24 + 1))                    # 1 day 1 second\n        print(humanize_time_delta(60 * 60 * 24 + 60 * 2 + 60*60*9 + 3)) # 1 day 9 hours 2 minutes 3 seconds\n    '
    if (sec < 0):
        logger.warn('humanize_time_delta() obtains negative seconds!')
        return '{:.3g} seconds'.format(sec)
    if (sec == 0):
        return '0 second'
    time = (datetime(2000, 1, 1) + timedelta(seconds=int(sec)))
    units = ['day', 'hour', 'minute', 'second']
    vals = [int((sec // 86400)), time.hour, time.minute, time.second]
    if (sec < 60):
        vals[(- 1)] = sec

    def _format(v, u):
        return '{:.3g} {}{}'.format(v, u, ('s' if (v > 1) else ''))
    ans = []
    for (v, u) in zip(vals, units):
        if (v > 0):
            ans.append(_format(v, u))
    return ' '.join(ans)
