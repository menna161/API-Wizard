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
def test_tabular1d_inverse():
    'Test that the Tabular1D inverse is defined'
    points = np.arange(5)
    values = np.array([1.5, 3.4, 6.7, 7, 32])
    t = models.Tabular1D(points, values)
    result = t.inverse((3.4, 6.7))
    assert_allclose(result, np.array((1.0, 2.0)))
    t2 = models.Tabular1D(points, values[::(- 1)])
    assert_allclose(t2.inverse.points[0], t2.lookup_table[::(- 1)])
    result2 = t2.inverse((7, 6.7))
    assert_allclose(result2, np.array((1.0, 2.0)))
    points = np.arange(5)
    values = np.array([1.5, 3.4, 3.4, 32, 25])
    t = models.Tabular1D(points, values)
    with pytest.raises(NotImplementedError):
        t.inverse((3.4, 7.0))
    table = np.arange((5 * 5)).reshape(5, 5)
    points = np.arange(0, 5)
    points = (points, points)
    t3 = models.Tabular2D(points=points, lookup_table=table)
    with pytest.raises(NotImplementedError):
        t3.inverse((3, 3))
    points = np.arange(5)
    values = np.array([1.5, 3.4, 6.7, 7, 32])
    t = models.Tabular1D(points, values)
    with pytest.raises(ValueError):
        t.inverse(100)
    t = models.Tabular1D(points, values, bounds_error=False, fill_value=None)
    result = t.inverse(100)
    assert_allclose(t(result), 100)
