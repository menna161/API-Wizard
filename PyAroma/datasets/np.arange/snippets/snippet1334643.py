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


def test_inconsistent_input_shapes():
    g = Gaussian2D()
    x = np.arange((- 1.0), 1, 0.2)
    y = x.copy()
    assert (np.abs((g(x, 0) - g(x, (0 * x)))).sum() == 0)
    x.shape = (10, 1)
    y.shape = (1, 10)
    with pytest.raises(ValueError):
        g(x, y)
