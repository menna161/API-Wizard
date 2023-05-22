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


def test_location_array(self):
    'Check that location arrays are checked for size and used\n        for the corresponding times.  Also checks that erfa\n        can handle array-valued locations, and can broadcast these if needed.\n        '
    lat = 19.48125
    lon = (- 155.933222)
    t = Time((['2006-01-15 21:24:37.5'] * 2), format='iso', scale='utc', precision=6, location=(lon, lat))
    assert np.all((t.utc.iso == '2006-01-15 21:24:37.500000'))
    assert np.all((t.tdb.iso[0] == '2006-01-15 21:25:42.684373'))
    t2 = Time((['2006-01-15 21:24:37.5'] * 2), format='iso', scale='utc', precision=6, location=(np.array([lon, 0]), np.array([lat, 0])))
    assert np.all((t2.utc.iso == '2006-01-15 21:24:37.500000'))
    assert (t2.tdb.iso[0] == '2006-01-15 21:25:42.684373')
    assert (t2.tdb.iso[1] != '2006-01-15 21:25:42.684373')
    with pytest.raises(ValueError):
        Time('2006-01-15 21:24:37.5', format='iso', scale='utc', precision=6, location=(np.array([lon, 0]), np.array([lat, 0])))
    with pytest.raises(ValueError):
        Time((['2006-01-15 21:24:37.5'] * 3), format='iso', scale='utc', precision=6, location=(np.array([lon, 0]), np.array([lat, 0])))
    mjd = np.arange(50000.0, 50008.0).reshape(4, 2)
    t3 = Time(mjd, format='mjd', scale='utc', location=(lon, lat))
    assert (t3.shape == (4, 2))
    assert (t3.location.shape == ())
    assert (t3.tdb.shape == t3.shape)
    t4 = Time(mjd, format='mjd', scale='utc', location=(np.array([lon, 0]), np.array([lat, 0])))
    assert (t4.shape == (4, 2))
    assert (t4.location.shape == t4.shape)
    assert (t4.tdb.shape == t4.shape)
    t5 = Time(mjd, format='mjd', scale='utc', location=(np.array([[lon], [0], [0], [0]]), np.array([[lat], [0], [0], [0]])))
    assert (t5.shape == (4, 2))
    assert (t5.location.shape == t5.shape)
    assert (t5.tdb.shape == t5.shape)
