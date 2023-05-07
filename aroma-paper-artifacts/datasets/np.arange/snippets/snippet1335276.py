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


def test_median_absolute_deviation():
    with NumpyRNGContext(12345):
        randvar = np.random.randn(10000)
        mad = funcs.median_absolute_deviation(randvar)
        randvar = randvar.reshape((10, 1000))
        mad = funcs.median_absolute_deviation(randvar, axis=1)
        assert (len(mad) == 10)
        assert (mad.size < randvar.size)
        mad = funcs.median_absolute_deviation(randvar, axis=0)
        assert (len(mad) == 1000)
        assert (mad.size < randvar.size)
        x = np.arange(((3 * 4) * 5))
        a = np.array([sum(x[:(i + 1)]) for i in range(len(x))]).reshape(3, 4, 5)
        mad = funcs.median_absolute_deviation(a)
        assert (mad == 389.5)
        mad = funcs.median_absolute_deviation(a, axis=0)
        assert_allclose(mad, [[210.0, 230.0, 250.0, 270.0, 290.0], [310.0, 330.0, 350.0, 370.0, 390.0], [410.0, 430.0, 450.0, 470.0, 490.0], [510.0, 530.0, 550.0, 570.0, 590.0]])
        mad = funcs.median_absolute_deviation(a, axis=1)
        assert_allclose(mad, [[27.5, 32.5, 37.5, 42.5, 47.5], [127.5, 132.5, 137.5, 142.5, 147.5], [227.5, 232.5, 237.5, 242.5, 247.5]])
        mad = funcs.median_absolute_deviation(a, axis=2)
        assert_allclose(mad, [[3.0, 8.0, 13.0, 18.0], [23.0, 28.0, 33.0, 38.0], [43.0, 48.0, 53.0, 58.0]])
