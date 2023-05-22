import os
import pytest
import numpy as np
from numpy.testing import assert_allclose, assert_almost_equal
from astropy.modeling import projections
from astropy.modeling.parameters import InputParameterError
from astropy import units as u
from astropy.io import fits
from astropy import wcs
from astropy.utils.data import get_pkg_data_filename
from astropy.tests.helper import assert_quantity_allclose


def test_c_projections_shaped():
    (nx, ny) = (5, 2)
    x = np.linspace(0, 1, nx)
    y = np.linspace(0, 1, ny)
    (xv, yv) = np.meshgrid(x, y)
    model = projections.Pix2Sky_TAN()
    (phi, theta) = model(xv, yv)
    assert_allclose(phi, [[0.0, 90.0, 90.0, 90.0, 90.0], [180.0, 165.96375653, 153.43494882, 143.13010235, 135.0]])
    assert_allclose(theta, [[90.0, 89.75000159, 89.50001269, 89.25004283, 89.00010152], [89.00010152, 88.96933478, 88.88210788, 88.75019826, 88.58607353]])
