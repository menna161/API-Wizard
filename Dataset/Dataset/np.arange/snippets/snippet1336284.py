import functools
import pytest
import numpy as np
from astropy.time import Time, TimeDelta
from astropy import units as u
from astropy.table import Column


def test_invalid_quantity_broadcast(self):
    'Check broadcasting rules in interactions with Quantity.'
    t0 = TimeDelta(np.arange(12.0).reshape(4, 3), format='sec')
    with pytest.raises(ValueError):
        (t0 + (np.arange(4.0) * u.s))
