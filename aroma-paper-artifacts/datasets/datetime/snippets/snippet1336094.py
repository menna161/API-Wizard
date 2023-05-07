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


def test_local_format_transforms(self):
    '\n        Test trasformation of local time to different formats\n        Transformation to formats with reference time should give\n        ScalevalueError\n        '
    t = Time('2006-01-15 21:24:37.5', scale='local')
    assert_allclose(t.jd, 2453751.3921006946, atol=((0.001 / 3600.0) / 24.0), rtol=0.0)
    assert_allclose(t.mjd, 53750.892100694444, atol=((0.001 / 3600.0) / 24.0), rtol=0.0)
    assert_allclose(t.decimalyear, 2006.0408002758752, atol=(((0.001 / 3600.0) / 24.0) / 365.0), rtol=0.0)
    assert (t.datetime == datetime.datetime(2006, 1, 15, 21, 24, 37, 500000))
    assert (t.isot == '2006-01-15T21:24:37.500')
    assert (t.yday == '2006:015:21:24:37.500')
    assert (t.fits == '2006-01-15T21:24:37.500')
    assert_allclose(t.byear, 2006.04217888831, atol=(((0.001 / 3600.0) / 24.0) / 365.0), rtol=0.0)
    assert_allclose(t.jyear, 2006.0407723496082, atol=(((0.001 / 3600.0) / 24.0) / 365.0), rtol=0.0)
    assert (t.byear_str == 'B2006.042')
    assert (t.jyear_str == 'J2006.041')
    with pytest.raises(ScaleValueError):
        t2 = t.gps
    with pytest.raises(ScaleValueError):
        t2 = t.unix
    with pytest.raises(ScaleValueError):
        t2 = t.cxcsec
    with pytest.raises(ScaleValueError):
        t2 = t.plot_date
