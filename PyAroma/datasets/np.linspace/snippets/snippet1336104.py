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


def test_broadcast_not_writable(self):
    val = (2458000 + np.arange(3))[(:, None)]
    val2 = np.linspace(0, 1, 4, endpoint=False)
    t = Time(val=val, val2=val2, format='jd', scale='tai')
    t_b = Time(val=(val + (0 * val2)), val2=((0 * val) + val2), format='jd', scale='tai')
    t_i = Time(val=57990, val2=0.3, format='jd', scale='tai')
    t_b[(1, 2)] = t_i
    t[(1, 2)] = t_i
    assert (t_b[(1, 2)] == t[(1, 2)]), 'writing worked'
    assert (t_b[(0, 2)] == t[(0, 2)]), "broadcasting didn't cause problems"
    assert (t_b[(1, 1)] == t[(1, 1)]), "broadcasting didn't cause problems"
    assert np.all((t_b == t)), 'behaved as expected'
