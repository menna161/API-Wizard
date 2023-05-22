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


def test_datetime64_no_format():
    dt64 = np.datetime64('2000-01-02T03:04:05.123456789')
    t = Time(dt64, scale='utc', precision=9)
    assert (t.iso == '2000-01-02 03:04:05.123456789')
    assert (t.datetime64 == dt64)
    assert (t.value == dt64)
