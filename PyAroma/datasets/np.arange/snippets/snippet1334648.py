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


def test_voigt_model():
    '\n    Currently just tests that the model peaks at its origin.\n    Regression test for https://github.com/astropy/astropy/issues/3942\n    '
    m = models.Voigt1D(x_0=5, amplitude_L=10, fwhm_L=0.5, fwhm_G=0.9)
    x = np.arange(0, 10, 0.01)
    y = m(x)
    assert (y[500] == y.max())
