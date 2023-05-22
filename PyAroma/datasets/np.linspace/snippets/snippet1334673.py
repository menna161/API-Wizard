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
def test_fitter1D(self, model_class, test_parameters):
    '\n        Test if the parametric model works with the fitter.\n        '
    x_lim = test_parameters['x_lim']
    parameters = test_parameters['parameters']
    model = create_model(model_class, test_parameters)
    if isinstance(parameters, dict):
        parameters = [parameters[name] for name in model.param_names]
    if ('log_fit' in test_parameters):
        if test_parameters['log_fit']:
            x = np.logspace(x_lim[0], x_lim[1], self.N)
    else:
        x = np.linspace(x_lim[0], x_lim[1], self.N)
    np.random.seed(0)
    relative_noise_amplitude = 0.01
    data = ((1 + (relative_noise_amplitude * np.random.randn(len(x)))) * model(x))
    fitter = fitting.LevMarLSQFitter()
    new_model = fitter(model, x, data)
    params = [getattr(new_model, name) for name in new_model.param_names]
    fixed = [param.fixed for param in params]
    expected = np.array([val for (val, fixed) in zip(parameters, fixed) if (not fixed)])
    fitted = np.array([param.value for param in params if (not param.fixed)])
    assert_allclose(fitted, expected, atol=self.fit_error)
