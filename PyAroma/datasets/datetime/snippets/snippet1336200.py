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


def test_set_format(self):
    '\n        Test basics of setting format attribute.\n        '
    dt = TimeDelta(86400.0, format='sec')
    assert (dt.value == 86400.0)
    assert (dt.format == 'sec')
    dt.format = 'jd'
    assert (dt.value == 1.0)
    assert (dt.format == 'jd')
    dt.format = 'datetime'
    assert (dt.value == timedelta(days=1))
    assert (dt.format == 'datetime')
