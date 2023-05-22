import pytest
import numpy as np
from numpy.testing import assert_equal, assert_allclose
from astropy import units as u
from astropy.stats.sigma_clipping import sigma_clip, SigmaClip, sigma_clipped_stats
from astropy.utils.exceptions import AstropyUserWarning
from astropy.utils.misc import NumpyRNGContext
from scipy import stats


def test_sigma_clip():
    with NumpyRNGContext(12345):
        randvar = np.random.randn(10000)
        filtered_data = sigma_clip(randvar, sigma=1, maxiters=2)
        assert (sum(filtered_data.mask) > 0)
        assert (sum((~ filtered_data.mask)) < randvar.size)
        filtered_data2 = sigma_clip(randvar, sigma=1, maxiters=2, stdfunc=np.var)
        assert (not np.all((filtered_data.mask == filtered_data2.mask)))
        filtered_data3 = sigma_clip(randvar, sigma=1, maxiters=2, cenfunc=np.mean)
        assert (not np.all((filtered_data.mask == filtered_data3.mask)))
        filtered_data = sigma_clip(randvar, sigma=3, maxiters=None)
        assert (filtered_data.data[0] == randvar[0])
        filtered_data.data[0] += 1.0
        assert (filtered_data.data[0] != randvar[0])
        filtered_data = sigma_clip(randvar, sigma=3, maxiters=None, copy=False)
        assert (filtered_data.data[0] == randvar[0])
        filtered_data.data[0] += 1.0
        assert (filtered_data.data[0] == randvar[0])
        data = ((np.arange(5) + np.random.normal(0.0, 0.05, (5, 5))) + np.diag(np.ones(5)))
        filtered_data = sigma_clip(data, axis=0, sigma=2.3)
        assert (filtered_data.count() == 20)
        filtered_data = sigma_clip(data, axis=1, sigma=2.3)
        assert (filtered_data.count() == 25)
