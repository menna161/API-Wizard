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


def test_Shift_model_set_linear_fit():
    'Test linear fitting of Shift model (issue #6103).'
    init_model = models.Shift(offset=[0, 0], n_models=2)
    x = np.arange(10)
    yy = np.array([(x + 0.1), (x - 0.2)])
    fitter = fitting.LinearLSQFitter()
    fitted_model = fitter(init_model, x, yy)
    assert_allclose(fitted_model.parameters, [0.1, (- 0.2)], atol=1e-15)
