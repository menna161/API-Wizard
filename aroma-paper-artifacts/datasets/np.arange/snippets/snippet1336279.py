import functools
import pytest
import numpy as np
from astropy.time import Time, TimeDelta
from astropy import units as u
from astropy.table import Column


def test_valid_quantity_operations1(self):
    'Check adding/substracting/comparing a time-valued quantity works\n        with a TimeDelta.  Addition/subtraction should give TimeDelta'
    t0 = TimeDelta(106400.0, format='sec')
    q1 = (10.0 * u.second)
    t1 = (t0 + q1)
    assert isinstance(t1, TimeDelta)
    assert (t1.value == (t0.value + q1.to_value(u.second)))
    q2 = (1.0 * u.day)
    t2 = (t0 - q2)
    assert isinstance(t2, TimeDelta)
    assert allclose_sec(t2.value, (t0.value - q2.to_value(u.second)))
    assert (t0 > q1)
    assert (t0 < (1.0 * u.yr))
    q3 = (np.arange(12.0).reshape(4, 3) * u.hour)
    t3 = (t0 + q3)
    assert isinstance(t3, TimeDelta)
    assert (t3.shape == q3.shape)
    assert allclose_sec(t3.value, (t0.value + q3.to_value(u.second)))
