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


def _phase_asfloat(date: datetime.date) -> float:
    jd = julianday(date)
    dt = (pow((jd - 2382148), 2) / (41048480 * 86400))
    t = (((jd + dt) - 2451545.0) / 36525)
    t2 = pow(t, 2)
    t3 = pow(t, 3)
    d = (((297.85 + (445267.1115 * t)) - (0.00163 * t2)) + (t3 / 545868))
    d = radians((d % 360.0))
    m = (357.53 + (35999.0503 * t))
    m = radians((m % 360.0))
    m1 = (((134.96 + (477198.8676 * t)) + (0.008997 * t2)) + (t3 / 69699))
    m1 = radians((m1 % 360.0))
    elong = (degrees(d) + (6.29 * sin(m1)))
    elong -= (2.1 * sin(m))
    elong += (1.27 * sin(((2 * d) - m1)))
    elong += (0.66 * sin((2 * d)))
    elong = (elong % 360.0)
    elong = int(elong)
    moon = (((elong + 6.43) / 360) * 28)
    return moon
