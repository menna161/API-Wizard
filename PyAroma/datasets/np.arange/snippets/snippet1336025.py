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


def test_bool():
    'Any Time object should evaluate to True unless it is empty [#3520].'
    t = Time(np.arange(50000, 50010), format='mjd', scale='utc')
    assert (bool(t) is True)
    assert (bool(t[0]) is True)
    assert (bool(t[:0]) is False)
