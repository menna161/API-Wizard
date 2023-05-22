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


def test_init_from_time_objects(self):
    'Initialize from one or more Time objects'
    t1 = Time('2007:001', scale='tai')
    t2 = Time(['2007-01-02', '2007-01-03'], scale='utc')
    t3 = Time([t1, t2])
    assert (len(t3) == 3)
    assert (t3.scale == t1.scale)
    assert (t3.format == t1.format)
    assert np.all((t3.value == np.concatenate([[t1.yday], t2.tai.yday])))
    t3 = Time(t1)
    assert t3.isscalar
    assert (t3.scale == t1.scale)
    assert (t3.format == t1.format)
    assert np.all((t3.value == t1.value))
    t3 = Time(t1, scale='utc')
    assert (t3.scale == 'utc')
    assert np.all((t3.value == t1.utc.value))
    t3 = Time([t1, t2], scale='tt')
    assert (t3.scale == 'tt')
    assert (t3.format == t1.format)
    assert np.all((t3.value == np.concatenate([[t1.tt.yday], t2.tt.yday])))
    mjd = np.arange(50000.0, 50006.0)
    frac = np.arange(0.0, 0.999, 0.2)
    t4 = Time((mjd[(:, np.newaxis)] + frac), format='mjd', scale='utc')
    t5 = Time([t4[:2], t4[4:5]])
    assert (t5.shape == (3, 5))
    with pytest.raises(ValueError):
        t6 = Time(t1, scale='local')
