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


def test_python_timedelta_scalar():
    td = timedelta(days=1, seconds=1)
    td1 = TimeDelta(td, format='datetime')
    assert (td1.sec == 86401.0)
    td2 = TimeDelta(86401.0, format='sec')
    assert (td2.datetime == td)
