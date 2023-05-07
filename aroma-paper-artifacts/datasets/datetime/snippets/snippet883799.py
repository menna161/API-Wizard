import asyncio
import datetime
import json
import os
import signal
import psutil
from i3hub import extension, listen, status_array_merge


def check(first_run):
    now = datetime.datetime.now()
    rv = False
    for (module, update_frequency) in modules:
        if (first_run or ((now.second % update_frequency) == 0)):
            result = module(now)
            if result:
                status_array_merge(self._current_status, result)
                rv = True
    return rv
