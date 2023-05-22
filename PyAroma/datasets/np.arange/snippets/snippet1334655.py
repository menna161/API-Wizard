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


@pytest.mark.skipif('not HAS_SCIPY_14')
def test_tabular_bounding_box_with_units():
    points = (np.arange(5) * u.pix)
    lt = (np.arange(5) * u.AA)
    t = models.Tabular1D(points, lt)
    result = t((1 * u.pix), with_bounding_box=True)
    assert (result == (1.0 * u.AA))
    assert (t.inverse(result, with_bounding_box=True) == (1 * u.pix))
