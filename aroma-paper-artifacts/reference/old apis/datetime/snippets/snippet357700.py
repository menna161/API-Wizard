import datetime
import re
from dataclasses import dataclass, field
from enum import Enum
from math import radians, tan
from typing import Optional, Tuple, Union
import zoneinfo
from backports import zoneinfo


def today(tz: Optional[datetime.tzinfo]=None) -> datetime.date:
    'Returns the current date in the specified time zone'
    return now(tz).date()
