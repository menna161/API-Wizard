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
@pytest.mark.filterwarnings('ignore:The fit may be unsuccessful.*')
@pytest.mark.parametrize('model', compound_models_no_units)
def test_compound_without_units(model):
    x = (np.linspace((- 5), 5, 10) * u.Angstrom)
    with NumpyRNGContext(12345):
        y = np.random.sample(10)
    fitter = fitting.LevMarLSQFitter()
    res_fit = fitter(model, x, (y * u.Hz))
    for param_name in res_fit.param_names:
        print(getattr(res_fit, param_name))
    assert all([res_fit[i]._has_units for i in range(3)])
    z = res_fit(x)
    assert isinstance(z, u.Quantity)
    res_fit = fitter(model, (np.arange(10) * u.Unit('Angstrom')), y)
    assert all([res_fit[i]._has_units for i in range(3)])
    z = res_fit(x)
    assert isinstance(z, np.ndarray)
