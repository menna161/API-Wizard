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


def test_datetime_tzinfo():
    '\n    Test #3160 that time zone info in datetime objects is respected.\n    '

    class TZm6(datetime.tzinfo):

        def utcoffset(self, dt):
            return datetime.timedelta(hours=(- 6))
    d = datetime.datetime(2002, 1, 2, 10, 3, 4, tzinfo=TZm6())
    t = Time(d)
    assert (t.value == datetime.datetime(2002, 1, 2, 16, 3, 4))
