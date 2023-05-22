import functools
import pytest
import numpy as np
from astropy.time import Time, TimeDelta
from astropy import units as u
from astropy.table import Column


def test_valid_quantity_operations2(self):
    'Check that TimeDelta is treated as a quantity where possible.'
    t0 = TimeDelta(100000.0, format='sec')
    f = (1.0 / t0)
    assert isinstance(f, u.Quantity)
    assert (f.unit == (1.0 / u.day))
    g = ((10.0 * u.m) / (u.second ** 2))
    v = (t0 * g)
    assert isinstance(v, u.Quantity)
    assert u.allclose(v, (((t0.sec * g.value) * u.m) / u.second))
    q = np.log10((t0 / u.second))
    assert isinstance(q, u.Quantity)
    assert (q.value == np.log10(t0.sec))
    s = (1.0 * u.m)
    v = (s / t0)
    assert isinstance(v, u.Quantity)
    assert u.allclose(v, (((1.0 / t0.sec) * u.m) / u.s))
    t = (1.0 * u.s)
    t2 = (t0 * t)
    assert isinstance(t2, u.Quantity)
    assert u.allclose(t2, (t0.sec * (u.s ** 2)))
    t3 = ([1] / t0)
    assert isinstance(t3, u.Quantity)
    assert u.allclose(t3, (1 / (t0.sec * u.s)))
    t1 = TimeDelta(np.arange(100000.0, 100012.0).reshape(6, 2), format='sec')
    f = ((np.array([1.0, 2.0]) * u.cycle) * u.Hz)
    phase = (f * t1)
    assert isinstance(phase, u.Quantity)
    assert (phase.shape == t1.shape)
    assert u.allclose(phase, ((t1.sec * f.value) * u.cycle))
    q = (t0 * t1)
    assert isinstance(q, u.Quantity)
    assert np.all((q == (t0.to(u.day) * t1.to(u.day))))
    q = (t1 / t0)
    assert isinstance(q, u.Quantity)
    assert np.all((q == (t1.to(u.day) / t0.to(u.day))))
