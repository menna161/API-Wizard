import datetime
from dataclasses import dataclass, field, replace
from math import asin, atan2, cos, degrees, fabs, pi, radians, sin, sqrt
from typing import Callable, List, Optional, Union
from astral import AstralBodyPosition, Observer, now, today
from astral.julian import julianday, julianday_2000
from astral.sidereal import lmst
from astral.table4 import Table4Row, table4_u, table4_v, table4_w
import zoneinfo
from backports import zoneinfo


def sgn(value1: Union[(float, datetime.timedelta)]) -> int:
    'Test whether value1 and value2 have the same sign'
    if isinstance(value1, datetime.timedelta):
        value1 = value1.total_seconds()
    if (value1 < 0):
        return (- 1)
    elif (value1 > 0):
        return 1
    else:
        return 0
