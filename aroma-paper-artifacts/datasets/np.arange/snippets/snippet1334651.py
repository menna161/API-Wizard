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
def test_tabular_interp_2d():
    table = np.array([[(- 0.04614432), (- 0.02512547), (- 0.00619557), 0.0144165, 0.0297525], [(- 0.04510594), (- 0.03183369), (- 0.01118008), 0.01201388, 0.02496205], [(- 0.05464094), (- 0.02804499), (- 0.00960086), 0.01134333, 0.02284104], [(- 0.04879338), (- 0.02539565), (- 0.00440462), 0.01795145, 0.02122417], [(- 0.03637372), (- 0.01630025), (- 0.00157902), 0.01649774, 0.01952131]])
    points = np.arange(0, 5)
    points = (points, points)
    xnew = np.array([0.0, 0.7, 1.4, 2.1, 3.9])
    LookupTable = models.tabular_model(2)
    model = LookupTable(points, table)
    znew = model(xnew, xnew)
    result = np.array([(- 0.04614432), (- 0.03450009), (- 0.02241028), (- 0.0069727), 0.01938675])
    assert_allclose(znew, result, atol=1e-07)
    a = np.arange(12).reshape((3, 4))
    (y, x) = np.mgrid[(:3, :4)]
    t = models.Tabular2D(lookup_table=a)
    r = t(y, x)
    assert_allclose(a, r)
    with pytest.raises(ValueError):
        model = LookupTable(points=([1.2, 2.3], [1.2, 6.7], [3, 4]))
    with pytest.raises(ValueError):
        model = LookupTable(lookup_table=[1, 2, 3])
    with pytest.raises(NotImplementedError):
        model = LookupTable(n_models=2)
    with pytest.raises(ValueError):
        model = LookupTable(([1, 2], [3, 4]), [5, 6])
    with pytest.raises(ValueError):
        model = LookupTable((([1, 2] * u.m), [3, 4]), [[5, 6], [7, 8]])
    with pytest.raises(ValueError):
        model = LookupTable(points, table, bounds_error=False, fill_value=(1 * u.Jy))
    points = (points[0] * u.nm)
    points = (points, points)
    xnew = (xnew * u.nm)
    model = LookupTable(points, (table * u.nJy))
    result = (result * u.nJy)
    assert_quantity_allclose(model(xnew, xnew), result, atol=(1e-07 * u.nJy))
    xnew = xnew.to(u.m)
    assert_quantity_allclose(model(xnew, xnew), result, atol=(1e-07 * u.nJy))
    bbox = ((0 * u.nm), (4 * u.nm))
    bbox = (bbox, bbox)
    assert (model.bounding_box == bbox)
