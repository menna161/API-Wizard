import numpy as np
import pytest
from astropy.modeling import models
from astropy import units as u
from astropy.units import UnitsError
from astropy.tests.helper import assert_quantity_allclose
from astropy.utils import NumpyRNGContext
from astropy.modeling import fitting
from scipy import optimize


def _fake_gaussian_data():
    with NumpyRNGContext(12345):
        x = np.linspace((- 5.0), 5.0, 2000)
        y = (3 * np.exp((((- 0.5) * ((x - 1.3) ** 2)) / (0.8 ** 2))))
        y += np.random.normal(0.0, 0.2, x.shape)
    x = (x * u.m)
    y = (y * u.Jy)
    return (x, y)
