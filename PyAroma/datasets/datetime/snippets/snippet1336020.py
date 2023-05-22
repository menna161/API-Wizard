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


def test_now():
    '\n    Tests creating a Time object with the `now` class method.\n    '
    now = datetime.datetime.utcnow()
    t = Time.now()
    assert (t.format == 'datetime')
    assert (t.scale == 'utc')
    dt = (t.datetime - now)
    assert (dt.total_seconds() < 0.1)
