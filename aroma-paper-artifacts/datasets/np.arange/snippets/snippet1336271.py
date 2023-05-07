import functools
import pytest
import numpy as np
from astropy.time import Time, TimeDelta
from astropy import units as u
from astropy.table import Column


def test_column_with_and_without_units(self):
    'Ensure a Column without a unit is treated as an array [#3648]'
    a = np.arange(50000.0, 50010.0)
    ta = Time(a, format='mjd')
    c1 = Column(np.arange(50000.0, 50010.0), name='mjd')
    tc1 = Time(c1, format='mjd')
    assert np.all((ta == tc1))
    c2 = Column(np.arange(50000.0, 50010.0), name='mjd', unit='day')
    tc2 = Time(c2, format='mjd')
    assert np.all((ta == tc2))
    c3 = Column(np.arange(50000.0, 50010.0), name='mjd', unit='m')
    with pytest.raises(u.UnitsError):
        Time(c3, format='mjd')
