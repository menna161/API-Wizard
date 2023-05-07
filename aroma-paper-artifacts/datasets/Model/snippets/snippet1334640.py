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
def test_custom_model(amplitude=4, frequency=1):

    def sine_model(x, amplitude=4, frequency=1):
        '\n        Model function\n        '
        return (amplitude * np.sin((((2 * np.pi) * frequency) * x)))

    def sine_deriv(x, amplitude=4, frequency=1):
        '\n        Jacobian of model function, e.g. derivative of the function with\n        respect to the *parameters*\n        '
        da = np.sin((((2 * np.pi) * frequency) * x))
        df = ((((2 * np.pi) * x) * amplitude) * np.cos((((2 * np.pi) * frequency) * x)))
        return np.vstack((da, df))
    SineModel = models.custom_model(sine_model, fit_deriv=sine_deriv)
    x = np.linspace(0, 4, 50)
    sin_model = SineModel()
    sin_model.evaluate(x, 5.0, 2.0)
    sin_model.fit_deriv(x, 5.0, 2.0)
    np.random.seed(0)
    data = ((sin_model(x) + np.random.rand(len(x))) - 0.5)
    fitter = fitting.LevMarLSQFitter()
    model = fitter(sin_model, x, data)
    assert np.all(((np.array([model.amplitude.value, model.frequency.value]) - np.array([amplitude, frequency])) < 0.001))
