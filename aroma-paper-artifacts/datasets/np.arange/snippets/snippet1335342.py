import pytest
import numpy as np
from numpy.testing import assert_equal, assert_allclose
from astropy.stats.jackknife import jackknife_resampling, jackknife_stats
from astropy.utils.exceptions import AstropyDeprecationWarning
import scipy


def test_jackknife_stats_exceptions():
    with pytest.raises(ValueError):
        with pytest.warns(AstropyDeprecationWarning):
            jackknife_stats(np.array([]), np.mean, conf_lvl=0.9)
    with pytest.raises(ValueError):
        jackknife_stats(np.arange(2), np.mean, confidence_level=42)
