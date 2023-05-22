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
def test_fit_with_bound_constraints_estimate_jacobian():
    '\n    Regression test for https://github.com/astropy/astropy/issues/2400\n\n    Checks that bounds constraints are obeyed on a custom model that does not\n    define fit_deriv (and thus its Jacobian must be estimated for non-linear\n    fitting).\n    '

    class MyModel(Fittable1DModel):
        a = Parameter(default=1)
        b = Parameter(default=2)

        @staticmethod
        def evaluate(x, a, b):
            return ((a * x) + b)
    m_real = MyModel(a=1.5, b=(- 3))
    x = np.arange(100)
    y = m_real(x)
    m = MyModel()
    f = fitting.LevMarLSQFitter()
    fitted_1 = f(m, x, y)
    assert np.allclose(fitted_1.a, 1.5)
    assert np.allclose(fitted_1.b, (- 3))
    m2 = MyModel()
    m2.a.bounds = ((- 2), 2)
    f2 = fitting.LevMarLSQFitter()
    fitted_2 = f2(m2, x, y)
    assert np.allclose(fitted_1.a, 1.5)
    assert np.allclose(fitted_1.b, (- 3))
    assert np.any((f2.fit_info['fjac'] != 0))
