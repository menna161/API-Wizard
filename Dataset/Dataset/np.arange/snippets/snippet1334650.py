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
def test_tabular_interp_1d():
    '\n    Test Tabular1D model.\n    '
    points = np.arange(0, 5)
    values = [1.0, 10, 2, 45, (- 3)]
    LookupTable = models.tabular_model(1)
    model = LookupTable(points=points, lookup_table=values)
    xnew = [0.0, 0.7, 1.4, 2.1, 3.9]
    ans1 = [1.0, 7.3, 6.8, 6.3, 1.8]
    assert_allclose(model(xnew), ans1)
    model = LookupTable(lookup_table=values)
    assert_allclose(model(xnew), ans1)
    xextrap = [0.0, 0.7, 1.4, 2.1, 3.9, 4.1]
    with pytest.raises(ValueError):
        model(xextrap)
    model = LookupTable(lookup_table=values, bounds_error=False, fill_value=None)
    assert_allclose(model(xextrap), [1.0, 7.3, 6.8, 6.3, 1.8, (- 7.8)])
    xnew = (xnew * u.nm)
    ans1 = (ans1 * u.nJy)
    model = LookupTable(points=(points * u.nm), lookup_table=(values * u.nJy))
    assert_quantity_allclose(model(xnew), ans1)
    assert_quantity_allclose(model(xnew.to(u.nm)), ans1)
    assert (model.bounding_box == ((0 * u.nm), (4 * u.nm)))
    model = LookupTable([1, 2, 3], ([10, 20, 30] * u.nJy), bounds_error=False, fill_value=(1e-33 * (u.W / ((u.m * u.m) * u.Hz))))
    assert_quantity_allclose(model(np.arange(5)), ([100, 10, 20, 30, 100] * u.nJy))
