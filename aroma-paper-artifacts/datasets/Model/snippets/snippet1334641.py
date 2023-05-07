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


def test_custom_model_init():

    @models.custom_model
    def SineModel(x, amplitude=4, frequency=1):
        'Model function'
        return (amplitude * np.sin((((2 * np.pi) * frequency) * x)))
    sin_model = SineModel(amplitude=2.0, frequency=0.5)
    assert (sin_model.amplitude == 2.0)
    assert (sin_model.frequency == 0.5)
