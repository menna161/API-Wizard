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


def test_ExponentialAndLogarithmic1D_fit():
    xarr = np.linspace(0.1, 10.0, 200)
    em_model = models.Exponential1D(amplitude=1, tau=1)
    log_model = models.Logarithmic1D(amplitude=1, tau=1)
    assert_allclose(xarr, em_model.inverse(em_model(xarr)))
    assert_allclose(xarr, log_model.inverse(log_model(xarr)))
