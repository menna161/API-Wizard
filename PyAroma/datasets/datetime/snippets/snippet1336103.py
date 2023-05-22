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


def test_val_broadcasts_against_val2(self):
    mjd = np.arange(50000.0, 50007.0)
    frac = np.arange(0.0, 0.999, 0.2)
    t = Time(mjd[(:, np.newaxis)], frac, format='mjd', scale='utc')
    assert (t.shape == (7, 5))
    with pytest.raises(ValueError):
        Time([0.0, 50000.0], [0.0, 1.0, 2.0], format='mjd', scale='tai')
