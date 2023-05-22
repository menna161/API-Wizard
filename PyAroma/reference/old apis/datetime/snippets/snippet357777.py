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


def phase(date: Optional[datetime.date]=None) -> float:
    "Calculates the phase of the moon on the specified date.\n\n    Args:\n        date: The date to calculate the phase for. Dates are always in the UTC timezone.\n              If not specified then today's date is used.\n\n    Returns:\n        A number designating the phase.\n\n        ============  ==============\n        0 .. 6.99     New moon\n        7 .. 13.99    First quarter\n        14 .. 20.99   Full moon\n        21 .. 27.99   Last quarter\n        ============  ==============\n    "
    if (date is None):
        date = today()
    moon = _phase_asfloat(date)
    if (moon >= 28.0):
        moon -= 28.0
    return moon
