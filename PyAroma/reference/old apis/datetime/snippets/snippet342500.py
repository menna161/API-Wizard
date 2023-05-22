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


def get_all_records(mac_address: str, entry_filter: dict, remove_empty: bool=False) -> Record:
    '\n    Get stored datapoints from device. Apply any filters requested\n    `entry_filter` is a dictionary that can have the following values:\n        `last`: int : Get last n entries\n        `start`: datetime : Get entries after specified time\n        `end`: datetime : Get entries before specified time\n        `temp`: bool : Get temperature data points (default = True)\n        `humi`: bool : Get humidity data points (default = True)\n        `pres`: bool : Get pressure data points (default = True)\n        `co2`: bool : Get co2 data points (default = True)\n    '
    return asyncio.run(_all_records(mac_address, entry_filter, remove_empty))
