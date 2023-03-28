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


def elevation(observer: Observer, at: Optional[datetime.datetime]=None):
    if (at is None):
        at = now()
    jd2000 = julianday_2000(at)
    position = moon_position(jd2000)
    lst0: Radians = radians(lmst(at, observer.longitude))
    hourangle: Radians = (lst0 - position.right_ascension)
    sh = sin(hourangle)
    ch = cos(hourangle)
    sd = sin(position.declination)
    cd = cos(position.declination)
    sl = sin(radians(observer.latitude))
    cl = cos(radians(observer.latitude))
    x = ((((- ch) * cd) * sl) + (sd * cl))
    y = ((- sh) * cd)
    z = (((ch * cd) * cl) + (sd * sl))
    r = sqrt(((x * x) + (y * y)))
    elevation = degrees(atan2(z, r))
    return elevation
