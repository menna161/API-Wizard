import pytest
import numpy as np
from numpy.testing import assert_allclose, assert_array_almost_equal_nulp, assert_equal
from astropy.stats.biweight import biweight_location, biweight_scale, biweight_midvariance, biweight_midcovariance, biweight_midcorrelation
from astropy.tests.helper import catch_warnings
from astropy.utils.misc import NumpyRNGContext


def test_biweight_midvariance_constant_axis_2d():
    shape = (10, 5)
    data = np.ones(shape)
    cbl = biweight_midvariance(data, axis=0)
    assert_allclose(cbl, np.zeros(shape[1]))
    cbl = biweight_midvariance(data, axis=1)
    assert_allclose(cbl, np.zeros(shape[0]))
    data = np.arange(50).reshape(10, 5)
    data[2] = 100.0
    data[7] = 2.0
    bw = biweight_midvariance(data, axis=1)
    assert_allclose(bw[2], 0.0)
    assert_allclose(bw[7], 0.0)
