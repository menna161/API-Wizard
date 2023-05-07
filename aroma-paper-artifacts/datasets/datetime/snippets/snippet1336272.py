import functools
import pytest
import numpy as np
from astropy.time import Time, TimeDelta
from astropy import units as u
from astropy.table import Column


def test_no_quantity_input_allowed(self):
    'Time formats that are not allowed to take Quantity input.'
    qy = (1990.0 * u.yr)
    for fmt in ('iso', 'yday', 'datetime', 'byear', 'byear_str', 'jyear_str'):
        with pytest.raises(ValueError):
            Time(qy, format=fmt, scale='utc')
