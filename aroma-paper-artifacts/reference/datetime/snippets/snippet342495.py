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


def _log_times(now, total, interval, ago):
    'Calculate the actual times datapoints were logged on device'
    times = []
    start = (now - datetime.timedelta(seconds=(((total - 1) * interval) + ago)))
    for idx in range(total):
        times.append((start + datetime.timedelta(seconds=(interval * idx))))
    return times
