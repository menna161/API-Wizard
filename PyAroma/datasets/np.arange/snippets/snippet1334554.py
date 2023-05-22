import pytest
import numpy as np
from numpy.testing import assert_allclose, assert_array_equal, assert_array_less
from astropy.modeling import models, InputParameterError
from astropy.coordinates import Angle
from astropy.modeling import fitting
from astropy.utils.exceptions import AstropyDeprecationWarning, AstropyUserWarning
from scipy import optimize
from astropy.stats.funcs import gaussian_sigma_to_fwhm
from astropy.modeling.functional_models import GAUSSIAN_SIGMA_TO_FWHM


@pytest.mark.skipif('not HAS_SCIPY')
def test_Shift_model_levmar_fit():
    'Test fitting Shift model with LevMarLSQFitter (issue #6103).'
    init_model = models.Shift()
    x = np.arange(10)
    y = (x + 0.1)
    fitter = fitting.LevMarLSQFitter()
    with pytest.warns(AstropyUserWarning, match='Model is linear in parameters'):
        fitted_model = fitter(init_model, x, y)
    assert_allclose(fitted_model.parameters, [0.1], atol=1e-15)
