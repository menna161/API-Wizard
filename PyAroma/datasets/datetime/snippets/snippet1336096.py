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


def test_datetime64(self):
    dt64 = np.datetime64('2000-01-02T03:04:05.123456789')
    dt64_2 = np.datetime64('2000-01-02')
    t = Time(dt64, scale='utc', precision=9, format='datetime64')
    assert (t.iso == '2000-01-02 03:04:05.123456789')
    assert (t.datetime64 == dt64)
    assert (t.value == dt64)
    t2 = Time(t.iso, scale='utc')
    assert (t2.datetime64 == dt64)
    t = Time(dt64_2, scale='utc', precision=3, format='datetime64')
    assert (t.iso == '2000-01-02 00:00:00.000')
    assert (t.datetime64 == dt64_2)
    assert (t.value == dt64_2)
    t2 = Time(t.iso, scale='utc')
    assert (t2.datetime64 == dt64_2)
    t = Time([dt64, dt64_2], scale='utc', format='datetime64')
    assert np.all((t.value == [dt64, dt64_2]))
    t = Time('2000-01-01 01:01:01.123456789', scale='tai')
    assert (t.datetime64 == np.datetime64('2000-01-01T01:01:01.123456789'))
    dt3 = (dt64 + ((dt64_2 - dt64) * np.arange(12))).reshape(4, 3)
    t3 = Time(dt3, scale='utc', format='datetime64')
    assert (t3.shape == (4, 3))
    assert (t3[(2, 1)].value == dt3[(2, 1)])
    assert (t3[(2, 1)] == Time(dt3[(2, 1)], format='datetime64'))
    assert np.all((t3.value == dt3))
    assert np.all((t3[1].value == dt3[1]))
    assert np.all((t3[(:, 2)] == Time(dt3[(:, 2)], format='datetime64')))
    assert (Time(t3[(2, 0)], format='datetime64') == t3[(2, 0)])
