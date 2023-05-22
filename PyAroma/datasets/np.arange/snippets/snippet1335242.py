import pytest
import numpy as np
from numpy.testing import assert_allclose, assert_array_almost_equal_nulp, assert_equal
from astropy.stats.biweight import biweight_location, biweight_scale, biweight_midvariance, biweight_midcovariance, biweight_midcorrelation
from astropy.tests.helper import catch_warnings
from astropy.utils.misc import NumpyRNGContext


def test_biweight_location_axis_tuple():
    'Test a 3D array with a tuple axis keyword.'
    data = np.arange(24).reshape(2, 3, 4)
    data[(0, 0)] = 100.0
    assert_equal(biweight_location(data, axis=0), biweight_location(data, axis=(0,)))
    assert_equal(biweight_location(data, axis=(- 1)), biweight_location(data, axis=(2,)))
    assert_equal(biweight_location(data, axis=(0, 1)), biweight_location(data, axis=(1, 0)))
    assert_equal(biweight_location(data, axis=(0, 2)), biweight_location(data, axis=(0, (- 1))))
    assert_equal(biweight_location(data, axis=(0, 1, 2)), biweight_location(data, axis=(2, 0, 1)))
    assert_equal(biweight_location(data, axis=(0, 1, 2)), biweight_location(data, axis=None))
