import datetime
import re
from dataclasses import dataclass, field
from enum import Enum
from math import radians, tan
from typing import Optional, Tuple, Union
import zoneinfo
from backports import zoneinfo


def time_to_seconds(value: datetime.time) -> float:
    'Convert a datetime.time to a floating point number of seconds'
    hours = time_to_hours(value)
    return (hours * 3600)
