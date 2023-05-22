import functools
import pytest
import numpy as np
from astropy.time import Time, TimeDelta
from astropy import units as u
from astropy.table import Column


def test_valid_quantity_operations(self):
    'Check that adding a time-valued quantity to a Time gives a Time'
    t0 = Time(100000.0, format='cxcsec')
    q1 = (10.0 * u.second)
    t1 = (t0 + q1)
    assert isinstance(t1, Time)
    assert (t1.value == (t0.value + q1.to_value(u.second)))
    q2 = (1.0 * u.day)
    t2 = (t0 - q2)
    assert allclose_sec(t2.value, (t0.value - q2.to_value(u.second)))
    q3 = (np.arange(15.0).reshape(3, 5) * u.hour)
    t3 = (t0 - q3)
    assert (t3.shape == q3.shape)
    assert allclose_sec(t3.value, (t0.value - q3.to_value(u.second)))
