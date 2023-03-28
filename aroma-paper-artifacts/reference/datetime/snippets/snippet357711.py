import datetime
from enum import Enum
from typing import Union


def day_fraction_to_time(fraction: float) -> datetime.time:
    s = (fraction * ((24 * 60) * 60))
    h = int((s / (60 * 60)))
    s -= ((h * 60) * 60)
    m = int((s / 60))
    s -= (m * 60)
    s = int(s)
    return datetime.time(h, m, s)
