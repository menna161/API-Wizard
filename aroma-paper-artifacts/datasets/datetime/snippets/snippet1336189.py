import functools
import itertools
import operator
from decimal import Decimal
from datetime import timedelta
import pytest
import numpy as np
from astropy.time import Time, TimeDelta, OperandTypeError, ScaleValueError, TIME_SCALES, STANDARD_TIME_SCALES, TIME_DELTA_SCALES
from astropy.utils import iers
from astropy import units as u


def test_timedelta_to_datetime():
    td = TimeDelta(1, format='jd')
    assert (td.to_datetime() == timedelta(days=1))
    td2 = TimeDelta([[1, 2], [3, 4]], format='jd')
    td = [[timedelta(days=1), timedelta(days=2)], [timedelta(days=3), timedelta(days=4)]]
    assert np.all((td2.to_datetime() == td))
