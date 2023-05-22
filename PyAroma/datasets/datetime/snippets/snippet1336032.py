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


def test_set_format_basic():
    '\n    Test basics of setting format attribute.\n    '
    for (format, value) in (('jd', 2451577.5), ('mjd', 51577.0), ('cxcsec', 65923264.184), ('datetime', datetime.datetime(2000, 2, 3, 0, 0)), ('iso', '2000-02-03 00:00:00.000')):
        t = Time('+02000-02-03', format='fits')
        t0 = t.replicate()
        t.format = format
        assert (t.value == value)
        assert (t._time.jd1 is t0._time.jd1)
        assert (t._time.jd2 is t0._time.jd2)
