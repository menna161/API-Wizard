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


def test_setitem_from_python_objects():
    t = Time([[1, 2], [3, 4]], format='cxcsec')
    assert (t.cache == {})
    t.iso
    assert ('iso' in t.cache['format'])
    assert np.all((t.iso == [['1998-01-01 00:00:01.000', '1998-01-01 00:00:02.000'], ['1998-01-01 00:00:03.000', '1998-01-01 00:00:04.000']]))
    t[(0, 1)] = 100
    assert (t.cache == {})
    assert allclose_sec(t.value, [[1, 100], [3, 4]])
    assert np.all((t.iso == [['1998-01-01 00:00:01.000', '1998-01-01 00:01:40.000'], ['1998-01-01 00:00:03.000', '1998-01-01 00:00:04.000']]))
    t.iso
    t[(1, :)] = 200
    assert (t.cache == {})
    assert allclose_sec(t.value, [[1, 100], [200, 200]])
    t[(:, 1)] = ['1998:002', '1998:003']
    assert allclose_sec(t.value, [[1, (86400 * 1)], [200, (86400 * 2)]])
    t = Time(['2000:001', '2000:002'])
    t[0] = '2001:001'
    with pytest.raises(ValueError) as err:
        t[0] = 100
    assert ('cannot convert value to a compatible Time object' in str(err.value))
