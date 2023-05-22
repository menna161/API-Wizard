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


def test_bounds_gauss2d_lsq(self):
    (X, Y) = np.meshgrid(np.arange(11), np.arange(11))
    bounds = {'x_mean': [0.0, 11.0], 'y_mean': [0.0, 11.0], 'x_stddev': [1.0, 4], 'y_stddev': [1.0, 4]}
    gauss = models.Gaussian2D(amplitude=10.0, x_mean=5.0, y_mean=5.0, x_stddev=4.0, y_stddev=4.0, theta=0.5, bounds=bounds)
    gauss_fit = fitting.LevMarLSQFitter()
    with pytest.warns(AstropyUserWarning, match='The fit may be unsuccessful'):
        model = gauss_fit(gauss, X, Y, self.data)
    x_mean = model.x_mean.value
    y_mean = model.y_mean.value
    x_stddev = model.x_stddev.value
    y_stddev = model.y_stddev.value
    assert ((x_mean + (10 ** (- 5))) >= bounds['x_mean'][0])
    assert ((x_mean - (10 ** (- 5))) <= bounds['x_mean'][1])
    assert ((y_mean + (10 ** (- 5))) >= bounds['y_mean'][0])
    assert ((y_mean - (10 ** (- 5))) <= bounds['y_mean'][1])
    assert ((x_stddev + (10 ** (- 5))) >= bounds['x_stddev'][0])
    assert ((x_stddev - (10 ** (- 5))) <= bounds['x_stddev'][1])
    assert ((y_stddev + (10 ** (- 5))) >= bounds['y_stddev'][0])
    assert ((y_stddev - (10 ** (- 5))) <= bounds['y_stddev'][1])
