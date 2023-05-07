import os
import copy
import functools
import datetime
from copy import deepcopy
from decimal import Decimal, localcontext
import numpy as np
from numpy.testing import assert_allclose
from astropy.tests.helper import catch_warnings, pytest
from astropy.utils.exceptions import AstropyDeprecationWarning, ErfaWarning
from astropy.utils import isiterable, iers
from astropy.time import Time, TimeDelta, ScaleValueError, STANDARD_TIME_SCALES, TimeString, TimezoneInfo
from astropy.coordinates import EarthLocation
from astropy import units as u
from astropy import _erfa as erfa
from astropy.table import Column, Table
import pytz


def test_datetime(self):
    '\n        Test datetime format, including guessing the format from the input type\n        by not providing the format keyword to Time.\n        '
    dt = datetime.datetime(2000, 1, 2, 3, 4, 5, 123456)
    dt2 = datetime.datetime(2001, 1, 1)
    t = Time(dt, scale='utc', precision=9)
    assert (t.iso == '2000-01-02 03:04:05.123456000')
    assert (t.datetime == dt)
    assert (t.value == dt)
    t2 = Time(t.iso, scale='utc')
    assert (t2.datetime == dt)
    t = Time([dt, dt2], scale='utc')
    assert np.all((t.value == [dt, dt2]))
    t = Time('2000-01-01 01:01:01.123456789', scale='tai')
    assert (t.datetime == datetime.datetime(2000, 1, 1, 1, 1, 1, 123457))
    dt3 = (dt + ((dt2 - dt) * np.arange(12))).reshape(4, 3)
    t3 = Time(dt3, scale='utc')
    assert (t3.shape == (4, 3))
    assert (t3[(2, 1)].value == dt3[(2, 1)])
    assert (t3[(2, 1)] == Time(dt3[(2, 1)]))
    assert np.all((t3.value == dt3))
    assert np.all((t3[1].value == dt3[1]))
    assert np.all((t3[(:, 2)] == Time(dt3[(:, 2)])))
    assert (Time(t3[(2, 0)]) == t3[(2, 0)])
