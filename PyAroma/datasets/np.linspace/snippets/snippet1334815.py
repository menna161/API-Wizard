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
@pytest.mark.parametrize('model', bad_compound_models_no_units)
def test_bad_compound_without_units(model):
    with pytest.raises(ValueError):
        x = (np.linspace((- 5), 5, 10) * u.Angstrom)
        with NumpyRNGContext(12345):
            y = np.random.sample(10)
        fitter = fitting.LevMarLSQFitter()
        res_fit = fitter(model, x, (y * u.Hz))
