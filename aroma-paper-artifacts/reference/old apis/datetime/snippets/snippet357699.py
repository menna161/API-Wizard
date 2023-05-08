import datetime
import re
from dataclasses import dataclass, field
from enum import Enum
from math import radians, tan
from typing import Optional, Tuple, Union
import zoneinfo
from backports import zoneinfo


def now(tz: Optional[datetime.tzinfo]=None) -> datetime.datetime:
    'Returns the current time in the specified time zone'
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    if (tz is None):
        return now_utc
    return now_utc.astimezone(tz)
