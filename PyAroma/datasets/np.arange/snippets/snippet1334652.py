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
def test_tabular_nd():
    a = np.arange(24).reshape((2, 3, 4))
    (x, y, z) = np.mgrid[(:2, :3, :4)]
    tab = models.tabular_model(3)
    t = tab(lookup_table=a)
    result = t(x, y, z)
    assert_allclose(a, result)
    with pytest.raises(ValueError):
        models.tabular_model(0)
