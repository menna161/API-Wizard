import pytest
import numpy as np
from numpy.testing import assert_allclose, assert_equal
from .example_models import models_1D, models_2D
from astropy.modeling import fitting, models
from astropy.modeling.models import Gaussian2D
from astropy.modeling.core import FittableModel
from astropy.modeling.parameters import Parameter
from astropy.modeling.polynomial import PolynomialBase
from astropy import units as u
from astropy.utils import minversion
from astropy.tests.helper import assert_quantity_allclose
from astropy.utils import NumpyRNGContext
import scipy


@pytest.mark.skipif('not HAS_SCIPY')
@pytest.mark.filterwarnings('ignore:.*:RuntimeWarning')
def test_deriv_1D(self, model_class, test_parameters):
    '\n        Test the derivative of a model by comparing results with an estimated\n        derivative.\n        '
    x_lim = test_parameters['x_lim']
    if (model_class.fit_deriv is None):
        pytest.skip('Derivative function is not defined for model.')
    if issubclass(model_class, PolynomialBase):
        pytest.skip('Skip testing derivative of polynomials.')
    if ('log_fit' in test_parameters):
        if test_parameters['log_fit']:
            x = np.logspace(x_lim[0], x_lim[1], self.N)
    else:
        x = np.linspace(x_lim[0], x_lim[1], self.N)
    parameters = test_parameters['parameters']
    model_with_deriv = create_model(model_class, test_parameters, use_constraints=False)
    model_no_deriv = create_model(model_class, test_parameters, use_constraints=False)
    rsn = np.random.RandomState(1234567890)
    n = ((0.1 * parameters[0]) * (rsn.rand(self.N) - 0.5))
    data = (model_with_deriv(x) + n)
    fitter_with_deriv = fitting.LevMarLSQFitter()
    new_model_with_deriv = fitter_with_deriv(model_with_deriv, x, data)
    fitter_no_deriv = fitting.LevMarLSQFitter()
    new_model_no_deriv = fitter_no_deriv(model_no_deriv, x, data, estimate_jacobian=True)
    assert_allclose(new_model_with_deriv.parameters, new_model_no_deriv.parameters, atol=0.15)
