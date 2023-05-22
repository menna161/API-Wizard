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


def test_broadcast_one_not_writable(self):
    val = (2458000 + np.arange(3))
    val2 = np.arange(1)
    t = Time(val=val, val2=val2, format='jd', scale='tai')
    t_b = Time(val=(val + (0 * val2)), val2=((0 * val) + val2), format='jd', scale='tai')
    t_i = Time(val=57990, val2=0.3, format='jd', scale='tai')
    t_b[1] = t_i
    t[1] = t_i
    assert (t_b[1] == t[1]), 'writing worked'
    assert (t_b[0] == t[0]), "broadcasting didn't cause problems"
    assert np.all((t_b == t)), 'behaved as expected'
