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
def test_KingProjectedAnalytic1D_fit():
    km = models.KingProjectedAnalytic1D(amplitude=1, r_core=1, r_tide=2)
    xarr = np.linspace(0.1, 2, 10)
    yarr = km(xarr)
    km_init = models.KingProjectedAnalytic1D(amplitude=1, r_core=1, r_tide=1)
    fitter = fitting.LevMarLSQFitter()
    km_fit = fitter(km_init, xarr, yarr)
    assert_allclose(km_fit.param_sets, km.param_sets)
