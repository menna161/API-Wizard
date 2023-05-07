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
def test_fit_with_fixed_and_bound_constraints():
    "\n    Regression test for https://github.com/astropy/astropy/issues/2235\n\n    Currently doesn't test that the fit is any *good*--just that parameters\n    stay within their given constraints.\n    "
    m = models.Gaussian1D(amplitude=3, mean=4, stddev=1, bounds={'mean': (4, 5)}, fixed={'amplitude': True})
    x = np.linspace(0, 10, 10)
    y = np.exp(((- (x ** 2)) / 2))
    f = fitting.LevMarLSQFitter()
    fitted_1 = f(m, x, y)
    assert (fitted_1.mean >= 4)
    assert (fitted_1.mean <= 5)
    assert (fitted_1.amplitude == 3.0)
    m.amplitude.fixed = False
    fitted_2 = f(m, x, y)
    assert (fitted_1.mean >= 4)
    assert (fitted_1.mean <= 5)
