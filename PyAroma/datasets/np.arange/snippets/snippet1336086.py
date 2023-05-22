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


def test_getitem(self):
    'Test that Time objects holding arrays are properly subscriptable,\n        set isscalar as appropriate, and also subscript delta_ut1_utc, etc.'
    mjd = np.arange(50000, 50010)
    t = Time(mjd, format='mjd', scale='utc', location=('45d', '50d'))
    t1 = t[3]
    assert (t1.isscalar is True)
    assert (t1._time.jd1 == t._time.jd1[3])
    assert (t1.location is t.location)
    t1a = Time(mjd[3], format='mjd', scale='utc')
    assert (t1a.isscalar is True)
    assert np.all((t1._time.jd1 == t1a._time.jd1))
    t1b = Time(t[3])
    assert (t1b.isscalar is True)
    assert np.all((t1._time.jd1 == t1b._time.jd1))
    t2 = t[4:6]
    assert (t2.isscalar is False)
    assert np.all((t2._time.jd1 == t._time.jd1[4:6]))
    assert (t2.location is t.location)
    t2a = Time(t[4:6])
    assert (t2a.isscalar is False)
    assert np.all((t2a._time.jd1 == t._time.jd1[4:6]))
    t2b = Time([t[4], t[5]])
    assert (t2b.isscalar is False)
    assert np.all((t2b._time.jd1 == t._time.jd1[4:6]))
    t2c = Time((t[4], t[5]))
    assert (t2c.isscalar is False)
    assert np.all((t2c._time.jd1 == t._time.jd1[4:6]))
    t.delta_tdb_tt = np.arange(len(t))
    t3 = t[4:6]
    assert np.all((t3._delta_tdb_tt == t._delta_tdb_tt[4:6]))
    t4 = Time(mjd, format='mjd', scale='utc', location=(np.arange(len(mjd)), np.arange(len(mjd))))
    t5 = t4[3]
    assert (t5.location == t4.location[3])
    t6 = t4[4:6]
    assert np.all((t6.location == t4.location[4:6]))
    allzeros = np.array((0.0, 0.0, 0.0), dtype=t4.location.dtype)
    assert (t6.location.view(np.ndarray)[(- 1)] != allzeros)
    assert (t4.location.view(np.ndarray)[5] != allzeros)
    t6.location.view(np.ndarray)[(- 1)] = allzeros
    assert (t4.location.view(np.ndarray)[5] == allzeros)
    frac = np.arange(0.0, 0.999, 0.2)
    t7 = Time((mjd[(:, np.newaxis)] + frac), format='mjd', scale='utc', location=('45d', '50d'))
    assert (t7[(0, 0)]._time.jd1 == t7._time.jd1[(0, 0)])
    assert (t7[(0, 0)].isscalar is True)
    assert np.all((t7[5]._time.jd1 == t7._time.jd1[5]))
    assert np.all((t7[5]._time.jd2 == t7._time.jd2[5]))
    assert np.all((t7[(:, 2)]._time.jd1 == t7._time.jd1[(:, 2)]))
    assert np.all((t7[(:, 2)]._time.jd2 == t7._time.jd2[(:, 2)]))
    assert np.all((t7[(:, 0)]._time.jd1 == t._time.jd1))
    assert np.all((t7[(:, 0)]._time.jd2 == t._time.jd2))
    t7_tdb = t7.tdb
    assert (t7_tdb[(0, 0)].delta_tdb_tt == t7_tdb.delta_tdb_tt[(0, 0)])
    assert np.all((t7_tdb[5].delta_tdb_tt == t7_tdb.delta_tdb_tt[5]))
    assert np.all((t7_tdb[(:, 2)].delta_tdb_tt == t7_tdb.delta_tdb_tt[(:, 2)]))
    t7.delta_tdb_tt = 0.1
    t7_tdb2 = t7.tdb
    assert (t7_tdb2[(0, 0)].delta_tdb_tt == 0.1)
    assert (t7_tdb2[5].delta_tdb_tt == 0.1)
    assert (t7_tdb2[(:, 2)].delta_tdb_tt == 0.1)
    t8 = Time((mjd[(:, np.newaxis)] + frac), format='mjd', scale='utc', location=(np.arange(len(frac)), np.arange(len(frac))))
    assert (t8[(0, 0)].location == t8.location[(0, 0)])
    assert np.all((t8[5].location == t8.location[5]))
    assert np.all((t8[(:, 2)].location == t8.location[(:, 2)]))
    t9 = t[:0]
    assert (t9.isscalar is False)
    assert (t9.shape == (0,))
    assert (t9.size == 0)
