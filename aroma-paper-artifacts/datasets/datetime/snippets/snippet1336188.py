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


def test_python_timedelta_vector():
    td = [[timedelta(days=1), timedelta(days=2)], [timedelta(days=3), timedelta(days=4)]]
    td1 = TimeDelta(td, format='datetime')
    assert np.all((td1.jd == [[1, 2], [3, 4]]))
    td2 = TimeDelta([[1, 2], [3, 4]], format='jd')
    assert np.all((td2.datetime == td))
