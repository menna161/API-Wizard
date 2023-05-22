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


def test_Trapezoid1D():
    'Regression test for https://github.com/astropy/astropy/issues/1721'
    model = models.Trapezoid1D(amplitude=4.2, x_0=2.0, width=1.0, slope=3)
    xx = np.linspace(0, 4, 8)
    yy = model(xx)
    yy_ref = [0.0, 1.41428571, 3.12857143, 4.2, 4.2, 3.12857143, 1.41428571, 0.0]
    assert_allclose(yy, yy_ref, rtol=0, atol=1e-06)
