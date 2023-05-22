import pytest
import numpy as np
from numpy.testing import assert_equal, assert_allclose
from astropy import units as u
from astropy.stats.sigma_clipping import sigma_clip, SigmaClip, sigma_clipped_stats
from astropy.utils.exceptions import AstropyUserWarning
from astropy.utils.misc import NumpyRNGContext
from scipy import stats


def test_sigma_clip_scalar_mask():
    'Test that the returned mask is not a scalar.'
    data = np.arange(5)
    result = sigma_clip(data, sigma=100.0, maxiters=1)
    assert (result.mask.shape != ())
