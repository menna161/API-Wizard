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


def test_epoch_date_jd_is_day_fraction():
    '\n    Ensure that jd1 and jd2 of an epoch Time are respect the (day, fraction) convention\n    (see #6638)\n    '
    t0 = Time('J2000', scale='tdb')
    assert (t0.jd1 == 2451545.0)
    assert (t0.jd2 == 0.0)
    t1 = Time(datetime.datetime(2000, 1, 1, 12, 0, 0), scale='tdb')
    assert (t1.jd1 == 2451545.0)
    assert (t1.jd2 == 0.0)
