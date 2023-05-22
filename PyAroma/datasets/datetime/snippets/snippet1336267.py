import functools
import decimal
import pytest
import numpy as np
from decimal import Decimal
from datetime import datetime
import astropy.units as u
import astropy._erfa as erfa
from astropy.time import Time, TimeDelta
from astropy.time.utils import day_frac, two_sum
from astropy.utils import iers
from astropy.utils.exceptions import ErfaWarning


def test_datetime_difference_agrees_with_timedelta():
    scale = 'tai'
    dt1 = datetime(1235, 1, 1, 0, 0)
    dt2 = datetime(9950, 1, 1, 0, 0, 0, 890773)
    t1 = Time(dt1, scale=scale)
    t2 = Time(dt2, scale=scale)
    assert (abs(((t2 - t1) - TimeDelta((dt2 - dt1), scale=scale))) < (1 * u.us))
