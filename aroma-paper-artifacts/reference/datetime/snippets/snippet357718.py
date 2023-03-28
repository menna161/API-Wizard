import datetime
from enum import Enum
from typing import Union


def _time_to_seconds(t: datetime.time) -> int:
    return int((((t.hour * 3600) + (t.minute * 60)) + t.second))
