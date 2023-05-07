import numpy as np
import pytest
from astropy.modeling import models
from astropy import units as u
from astropy.units import UnitsError
from astropy.tests.helper import assert_quantity_allclose
from astropy.utils import NumpyRNGContext
from astropy.modeling import fitting
from scipy import optimize


@pytest.mark.skipif('not HAS_SCIPY')
def test_compound_fitting_with_units():
    x = (np.linspace((- 5), 5, 15) * u.Angstrom)
    y = (np.linspace((- 5), 5, 15) * u.Angstrom)
    fitter = fitting.LevMarLSQFitter()
    m = models.Gaussian2D((10 * u.Hz), (3 * u.Angstrom), (4 * u.Angstrom), (1 * u.Angstrom), (2 * u.Angstrom))
    p = models.Planar2D(((3 * u.Hz) / u.Angstrom), ((4 * u.Hz) / u.Angstrom), (1 * u.Hz))
    model = (m + p)
    z = model(x, y)
    res = fitter(model, x, y, z)
    assert isinstance(res(x, y), np.ndarray)
    assert all([res[i]._has_units for i in range(2)])
    model = (models.Gaussian2D() + models.Planar2D())
    res = fitter(model, x, y, z)
    assert isinstance(res(x, y), np.ndarray)
    assert all([res[i]._has_units for i in range(2)])
