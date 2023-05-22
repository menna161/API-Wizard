import pytest
import numpy as np
from numpy.testing import assert_equal, assert_allclose
from astropy import units as u
from astropy.stats.sigma_clipping import sigma_clip, SigmaClip, sigma_clipped_stats
from astropy.utils.exceptions import AstropyUserWarning
from astropy.utils.misc import NumpyRNGContext
from scipy import stats


def test_sigma_clipped_stats():
    'Test list data with input mask or mask_value (#3268).'
    data = [0, 1]
    mask = np.array([True, False])
    result = sigma_clipped_stats(data, mask=mask)
    assert isinstance(result[1], float)
    assert (result == (1.0, 1.0, 0.0))
    result2 = sigma_clipped_stats(data, mask=mask, axis=0)
    assert_equal(result, result2)
    result = sigma_clipped_stats(data, mask_value=0.0)
    assert isinstance(result[1], float)
    assert (result == (1.0, 1.0, 0.0))
    data = [0, 2]
    result = sigma_clipped_stats(data)
    assert isinstance(result[1], float)
    assert (result == (1.0, 1.0, 1.0))
    _data = np.arange(10)
    data = np.ma.MaskedArray([_data, _data, (10 * _data)])
    mean = sigma_clip(data, axis=0, sigma=1).mean(axis=0)
    assert_equal(mean, _data)
    (mean, median, stddev) = sigma_clipped_stats(data, axis=0, sigma=1)
    assert_equal(mean, _data)
    assert_equal(median, _data)
    assert_equal(stddev, np.zeros_like(_data))
