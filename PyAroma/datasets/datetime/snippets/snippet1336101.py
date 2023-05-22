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


@pytest.mark.parametrize('d', [dict(val='2001:001', val2='ignored', scale='utc'), dict(val={'year': 2015, 'month': 2, 'day': 3, 'hour': 12, 'minute': 13, 'second': 14.567}, val2='ignored', scale='utc'), dict(val=np.datetime64('2005-02-25'), val2='ignored', scale='utc'), dict(val=datetime.datetime(2000, 1, 2, 12, 0, 0), val2='ignored', scale='utc')])
def test_unused_val2_raises(self, d):
    "Test that providing val2 is for string input lets user know we won't use it"
    with pytest.raises(ValueError):
        Time(**d)
