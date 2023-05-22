import asyncio
import datetime
import json
import os
import signal
import psutil
from i3hub import extension, listen, status_array_merge


def __init__(self, i3):
    self._i3 = i3
    self._disabled_widgets = None
    self._loop = i3.event_loop
    self._stop_sig = None
    self._cont_sig = None
    self._updating = False
    self._proc_net_route = None
    self._current_status = []
    self._counters = psutil.net_io_counters(pernic=True, nowrap=True)
    self._counters_timestamp = datetime.datetime.now().timestamp()
