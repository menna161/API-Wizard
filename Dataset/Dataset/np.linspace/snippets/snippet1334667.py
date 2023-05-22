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
def test_fitter2D(self, model_class, test_parameters):
    'Test if the parametric model works with the fitter.'
    x_lim = test_parameters['x_lim']
    y_lim = test_parameters['y_lim']
    parameters = test_parameters['parameters']
    model = create_model(model_class, test_parameters)
    if isinstance(parameters, dict):
        parameters = [parameters[name] for name in model.param_names]
    if ('log_fit' in test_parameters):
        if test_parameters['log_fit']:
            x = np.logspace(x_lim[0], x_lim[1], self.N)
            y = np.logspace(y_lim[0], y_lim[1], self.N)
    else:
        x = np.linspace(x_lim[0], x_lim[1], self.N)
        y = np.linspace(y_lim[0], y_lim[1], self.N)
    (xv, yv) = np.meshgrid(x, y)
    np.random.seed(0)
    noise = (np.random.rand(self.N, self.N) - 0.5)
    data = (model(xv, yv) + ((0.1 * parameters[0]) * noise))
    fitter = fitting.LevMarLSQFitter()
    new_model = fitter(model, xv, yv, data)
    params = [getattr(new_model, name) for name in new_model.param_names]
    fixed = [param.fixed for param in params]
    expected = np.array([val for (val, fixed) in zip(parameters, fixed) if (not fixed)])
    fitted = np.array([param.value for param in params if (not param.fixed)])
    assert_allclose(fitted, expected, atol=self.fit_error)
