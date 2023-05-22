import functools
import itertools
import operator
from decimal import Decimal
from datetime import timedelta
import pytest
import numpy as np
from astropy.time import Time, TimeDelta, OperandTypeError, ScaleValueError, TIME_SCALES, STANDARD_TIME_SCALES, TIME_DELTA_SCALES
from astropy.utils import iers
from astropy import units as u


def test_mul_div(self):
    for dt in (self.dt, self.dt_array):
        dt2 = ((dt + dt) + dt)
        dt3 = (3.0 * dt)
        assert allclose_jd(dt2.jd, dt3.jd)
        dt4 = (dt3 / 3.0)
        assert allclose_jd(dt4.jd, dt.jd)
    dt5 = (self.dt * np.arange(3))
    assert (dt5[0].jd == 0.0)
    assert (dt5[(- 1)].jd == (self.dt + self.dt).jd)
    dt6 = (self.dt * [0, 1, 2])
    assert np.all((dt6.jd == dt5.jd))
    with pytest.raises(OperandTypeError):
        (self.dt * self.t)
    with pytest.raises(TypeError):
        (self.dt * object())
