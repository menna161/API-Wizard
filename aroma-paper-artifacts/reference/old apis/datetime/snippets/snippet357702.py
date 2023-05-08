import datetime
import re
from dataclasses import dataclass, field
from enum import Enum
from math import radians, tan
from typing import Optional, Tuple, Union
import zoneinfo
from backports import zoneinfo


def hours_to_time(value: float) -> datetime.time:
    'Convert a floating point number of hours to a datetime.time'
    hour = int(value)
    value -= hour
    value *= 60
    minute = int(value)
    value -= minute
    value *= 60
    second = int(value)
    value -= second
    microsecond = int((value * 1000000))
    return datetime.time(hour, minute, second, microsecond)
