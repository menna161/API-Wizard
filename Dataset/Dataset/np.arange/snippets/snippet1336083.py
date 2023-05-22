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


def test_different_dimensions(self):
    'Test scalars, vector, and higher-dimensions'
    (val, val1) = (2450000.0, 0.125)
    t1 = Time(val, val1, format='jd')
    assert ((t1.isscalar is True) and (t1.shape == ()))
    val = np.arange(2450000.0, 2450010.0)
    t2 = Time(val, format='jd')
    assert ((t2.isscalar is False) and (t2.shape == val.shape))
    val2 = 0.0
    t3 = Time(val, val2, format='jd')
    assert ((t3.isscalar is False) and (t3.shape == val.shape))
    val2 = (np.arange(5.0) / 10.0).reshape(5, 1)
    t4 = Time(val, val2, format='jd')
    assert (t4.isscalar is False)
    assert (t4.shape == np.broadcast(val, val2).shape)
