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


def test_properties(self):
    'Use properties to convert scales and formats.  Note that the UT1 to\n        UTC transformation requires a supplementary value (``delta_ut1_utc``)\n        that can be obtained by interpolating from a table supplied by IERS.\n        This is tested separately.'
    t = Time('2010-01-01 00:00:00', format='iso', scale='utc')
    t.delta_ut1_utc = 0.3341
    assert allclose_jd(t.jd, 2455197.5)
    assert (t.iso == '2010-01-01 00:00:00.000')
    assert (t.tt.iso == '2010-01-01 00:01:06.184')
    assert (t.tai.fits == '2010-01-01T00:00:34.000')
    assert allclose_jd(t.utc.jd, 2455197.5)
    assert allclose_jd(t.ut1.jd, 2455197.500003867)
    assert (t.tcg.isot == '2010-01-01T00:01:06.910')
    assert allclose_sec(t.unix, 1262304000.0)
    assert allclose_sec(t.cxcsec, 378691266.184)
    assert allclose_sec(t.gps, 946339215.0)
    assert (t.datetime == datetime.datetime(2010, 1, 1))
