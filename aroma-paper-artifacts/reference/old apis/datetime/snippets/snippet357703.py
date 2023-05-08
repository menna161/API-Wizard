import datetime
import re
from dataclasses import dataclass, field
from enum import Enum
from math import radians, tan
from typing import Optional, Tuple, Union
import zoneinfo
from backports import zoneinfo


def time_to_hours(value: datetime.time) -> float:
    'Convert a datetime.time to a floating point number of hours'
    hours = 0.0
    hours += value.hour
    hours += (value.minute / 60)
    hours += (value.second / 3600)
    hours += (value.microsecond / 1000000)
    return hours
