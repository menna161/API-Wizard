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


def _attach_tzinfo(dt: datetime) -> datetime:
    if (dt and (not dt.tzinfo)):
        now = datetime.datetime.now().astimezone()
        dt = dt.replace(tzinfo=now.tzinfo)
    return dt
