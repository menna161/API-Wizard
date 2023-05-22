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
def test_Voigt1D():
    voi = models.Voigt1D(amplitude_L=(- 0.5), x_0=1.0, fwhm_L=5.0, fwhm_G=5.0)
    xarr = np.linspace((- 5.0), 5.0, num=40)
    yarr = voi(xarr)
    voi_init = models.Voigt1D(amplitude_L=(- 1.0), x_0=1.0, fwhm_L=5.0, fwhm_G=5.0)
    fitter = fitting.LevMarLSQFitter()
    voi_fit = fitter(voi_init, xarr, yarr)
    assert_allclose(voi_fit.param_sets, voi.param_sets)
