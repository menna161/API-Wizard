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


def test_ScaleModel():
    m = models.Scale(42)
    assert (m(0) == 0)
    assert_equal(m([1, 2]), [42, 84])
    m = models.Scale([42, 43], n_models=2)
    assert_equal(m(0), [0, 0])
    assert_equal(m([1, 2], model_set_axis=False), [[42, 84], [43, 86]])