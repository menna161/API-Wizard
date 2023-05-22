import types
import pytest
import numpy as np
from numpy.testing import assert_allclose
from numpy.random import RandomState
from astropy.modeling.core import Fittable1DModel
from astropy.modeling.parameters import Parameter
from astropy.modeling import models
from astropy.modeling import fitting
from astropy.utils.exceptions import AstropyUserWarning
from .utils import ignore_non_integer_warning
from scipy import optimize
from astropy.utils import NumpyRNGContext


@pytest.mark.skipif('not HAS_SCIPY')
@pytest.mark.filterwarnings('ignore:Model is linear in parameters.*')
def test_2d_model():
    from astropy.utils import NumpyRNGContext
    gauss2d = models.Gaussian2D(10.2, 4.3, 5, 2, 1.2, 1.4)
    fitter = fitting.LevMarLSQFitter()
    X = np.linspace((- 1), 7, 200)
    Y = np.linspace((- 1), 7, 200)
    (x, y) = np.meshgrid(X, Y)
    z = gauss2d(x, y)
    w = np.ones(x.size)
    w.shape = x.shape
    with NumpyRNGContext(1234567890):
        n = np.random.randn(x.size)
        n.shape = x.shape
        m = fitter(gauss2d, x, y, (z + (2 * n)), weights=w)
        assert_allclose(m.parameters, gauss2d.parameters, rtol=0.05)
        m = fitter(gauss2d, x, y, (z + (2 * n)), weights=None)
        assert_allclose(m.parameters, gauss2d.parameters, rtol=0.05)
        gauss2d.x_stddev.fixed = True
        m = fitter(gauss2d, x, y, (z + (2 * n)), weights=w)
        assert_allclose(m.parameters, gauss2d.parameters, rtol=0.05)
        m = fitter(gauss2d, x, y, (z + (2 * n)), weights=None)
        assert_allclose(m.parameters, gauss2d.parameters, rtol=0.05)
        p2 = models.Polynomial2D(1, c0_0=1, c1_0=1.2, c0_1=3.2)
        z = p2(x, y)
        m = fitter(p2, x, y, (z + (2 * n)), weights=None)
        assert_allclose(m.parameters, p2.parameters, rtol=0.05)
        m = fitter(p2, x, y, (z + (2 * n)), weights=w)
        assert_allclose(m.parameters, p2.parameters, rtol=0.05)
        p2.c1_0.fixed = True
        m = fitter(p2, x, y, (z + (2 * n)), weights=w)
        assert_allclose(m.parameters, p2.parameters, rtol=0.05)
        m = fitter(p2, x, y, (z + (2 * n)), weights=None)
        assert_allclose(m.parameters, p2.parameters, rtol=0.05)
