import pytest
import numpy as np
from numpy.testing import assert_equal, assert_allclose
from astropy.stats import funcs
from astropy import units as u
from astropy.tests.helper import catch_warnings
from astropy.utils.exceptions import AstropyDeprecationWarning
from astropy.utils.misc import NumpyRNGContext
import scipy
import mpmath
from scipy.stats import spearmanr


def test_median_absolute_deviation_multidim_axis():
    array = (np.ones((5, 4, 3)) * np.arange(5)[(:, np.newaxis, np.newaxis)])
    mad1 = funcs.median_absolute_deviation(array, axis=(1, 2))
    mad2 = funcs.median_absolute_deviation(array, axis=(2, 1))
    assert_equal(mad1, np.zeros(5))
    assert_equal(mad1, mad2)
