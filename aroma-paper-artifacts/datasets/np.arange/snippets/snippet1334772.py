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


def test_c_projection_striding():
    coords = np.arange(10).reshape((5, 2))
    model = projections.Sky2Pix_ZenithalPerspective(2, 30)
    (phi, theta) = model(coords[(:, 0)], coords[(:, 1)])
    assert_almost_equal(phi, [0.0, 2.2790416, 4.4889294, 6.6250643, 8.68301])
    assert_almost_equal(theta, [(- 76.4816918), (- 75.3594654), (- 74.1256332), (- 72.784558), (- 71.3406629)])
