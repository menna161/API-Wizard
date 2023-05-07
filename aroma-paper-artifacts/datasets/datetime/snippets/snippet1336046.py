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


def test_setitem_location():
    loc = EarthLocation(x=([1, 2] * u.m), y=([3, 4] * u.m), z=([5, 6] * u.m))
    t = Time([[1, 2], [3, 4]], format='cxcsec', location=loc)
    t[(0, 0)] = 0
    assert allclose_sec(t.value, [[0, 2], [3, 4]])
    with pytest.raises(ValueError) as err:
        t[(0, 0)] = Time((- 1), format='cxcsec')
    assert ('cannot set to Time with different location: expected location={} and got location=None'.format(loc[0]) in str(err.value))
    t[(0, 0)] = Time((- 2), format='cxcsec', location=loc[0])
    assert allclose_sec(t.value, [[(- 2), 2], [3, 4]])
    with pytest.raises(ValueError) as err:
        t[(0, 0)] = Time((- 2), format='cxcsec', location=loc[1])
    assert ('cannot set to Time with different location: expected location={} and got location={}'.format(loc[0], loc[1]) in str(err.value))
    t = Time([[1, 2], [3, 4]], format='cxcsec')
    with pytest.raises(ValueError) as err:
        t[(0, 0)] = Time((- 2), format='cxcsec', location=loc[1])
    assert ('cannot set to Time with different location: expected location=None and got location={}'.format(loc[1]) in str(err.value))
    t = Time([[1, 2], [3, 4]], format='cxcsec', location=loc)
    t[(0, :)] = Time([(- 3), (- 4)], format='cxcsec', location=loc)
    assert allclose_sec(t.value, [[(- 3), (- 4)], [3, 4]])
