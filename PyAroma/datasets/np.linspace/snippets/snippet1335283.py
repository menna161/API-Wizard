import pytest
import numpy as np
from numpy.testing import assert_equal, assert_allclose
from astropy.stats import funcs
from astropy import units as u
from astropy.tests.helper import catch_warnings
from astropy.utils.exceptions import AstropyDeprecationWarning
from astropy.utils.misc import NumpyRNGContext
import scipy
import mpmath
from scipy.stats import spearmanr


@pytest.mark.skipif('not HAS_SCIPY')
def test_binned_binom_proportion():
    nbins = 20
    x = np.linspace(0.0, 10.0, 100)
    success = np.ones(len(x), dtype=bool)
    (bin_ctr, bin_hw, p, perr) = funcs.binned_binom_proportion(x, success, bins=nbins)
    assert (bin_ctr.shape == (nbins,))
    assert (bin_hw.shape == (nbins,))
    assert (p.shape == (nbins,))
    assert (perr.shape == (2, nbins))
    assert (p == 1.0).all()
    success[:] = False
    (bin_ctr, bin_hw, p, perr) = funcs.binned_binom_proportion(x, success, bins=nbins)
    assert (p == 0.0).all()
