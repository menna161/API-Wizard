import asyncio
from dataclasses import dataclass, field
import datetime
from enum import IntEnum
import re
import struct
from typing import List, NamedTuple
from bleak import BleakClient
from bleak import BleakScanner
from bleak.backends.device import BLEDevice


def _calc_start_end(datapoint_times: int, entry_filter):
    '\n    Apply filters to get required start and end datapoint.\n    `entry_filter` is a dictionary that can have the following values:\n        `last`: int : Get last n entries\n        `start`: datetime : Get entries after specified time\n        `end`: datetime : Get entries before specified time\n    '
    last_n_entries = entry_filter.get('last')
    filter_start = _attach_tzinfo(entry_filter.get('start'))
    filter_end = _attach_tzinfo(entry_filter.get('end'))
    start = 1
    end = len(datapoint_times)
    if last_n_entries:
        start = max(((end - last_n_entries) + 1), start)
    if filter_start:
        time_start = (- 1)
        for (idx, timestamp) in enumerate(datapoint_times, start=1):
            if (filter_start <= timestamp):
                time_start = idx
                break
        if (0 < time_start <= end):
            start = time_start
        else:
            start = (- 1)
    if filter_end:
        time_end = (- 1)
        for (idx, timestamp) in enumerate(datapoint_times, start=1):
            if (timestamp <= filter_end):
                time_end = idx
            else:
                break
        if (start <= time_end <= end):
            end = time_end
        else:
            end = (- 1)
    return (start, end)
