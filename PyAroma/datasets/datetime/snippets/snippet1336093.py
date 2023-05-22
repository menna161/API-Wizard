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


def test_creating_all_formats(self):
    'Create a time object using each defined format'
    Time(2000.5, format='decimalyear')
    Time(100.0, format='cxcsec')
    Time(100.0, format='unix')
    Time(100.0, format='gps')
    Time(1950.0, format='byear', scale='tai')
    Time(2000.0, format='jyear', scale='tai')
    Time('B1950.0', format='byear_str', scale='tai')
    Time('J2000.0', format='jyear_str', scale='tai')
    Time('2000-01-01 12:23:34.0', format='iso', scale='tai')
    Time('2000-01-01 12:23:34.0Z', format='iso', scale='utc')
    Time('2000-01-01T12:23:34.0', format='isot', scale='tai')
    Time('2000-01-01T12:23:34.0Z', format='isot', scale='utc')
    Time('2000-01-01T12:23:34.0', format='fits')
    Time('2000-01-01T12:23:34.0', format='fits', scale='tdb')
    Time(2400000.5, 51544.0333981, format='jd', scale='tai')
    Time(0.0, 51544.0333981, format='mjd', scale='tai')
    Time('2000:001:12:23:34.0', format='yday', scale='tai')
    Time('2000:001:12:23:34.0Z', format='yday', scale='utc')
    dt = datetime.datetime(2000, 1, 2, 3, 4, 5, 123456)
    Time(dt, format='datetime', scale='tai')
    Time([dt, dt], format='datetime', scale='tai')
    dt64 = np.datetime64('2012-06-18T02:00:05.453000000', format='datetime64')
    Time(dt64, format='datetime64', scale='tai')
    Time([dt64, dt64], format='datetime64', scale='tai')
