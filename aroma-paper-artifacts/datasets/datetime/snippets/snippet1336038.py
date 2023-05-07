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


def test_to_datetime():
    tz = TimezoneInfo(utc_offset=((- 10) * u.hour), tzname='US/Hawaii')
    time = Time('2010-09-03 00:00:00')
    tz_aware_datetime = time.to_datetime(tz)
    assert (tz_aware_datetime.time() == datetime.time(14, 0))
    forced_to_astropy_time = Time(tz_aware_datetime)
    assert (tz.tzname(time.datetime) == tz_aware_datetime.tzname())
    assert (time == forced_to_astropy_time)
    time = Time(['2010-09-03 00:00:00', '2005-09-03 06:00:00', '1990-09-03 06:00:00'])
    tz_aware_datetime = time.to_datetime(tz)
    forced_to_astropy_time = Time(tz_aware_datetime)
    for (dt, tz_dt) in zip(time.datetime, tz_aware_datetime):
        assert (tz.tzname(dt) == tz_dt.tzname())
    assert np.all((time == forced_to_astropy_time))
    with pytest.raises(ValueError, match='does not support leap seconds'):
        Time('2015-06-30 23:59:60.000').to_datetime()
