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


def test_len_size():
    'Check length of Time objects and that scalar ones do not have one.'
    t = Time(np.arange(50000, 50010), format='mjd', scale='utc')
    assert ((len(t) == 10) and (t.size == 10))
    t1 = Time(np.arange(50000, 50010).reshape(2, 5), format='mjd', scale='utc')
    assert ((len(t1) == 2) and (t1.size == 10))
    t2 = t[:1]
    assert ((len(t2) == 1) and (t2.size == 1))
    t3 = t[:0]
    assert ((len(t3) == 0) and (t3.size == 0))
    t4 = t[0]
    with pytest.raises(TypeError) as err:
        len(t4)
    assert ('Time' in str(err.value))
