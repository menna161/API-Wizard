import pytest
import numpy as np
from numpy.testing import assert_equal, assert_allclose
from astropy import units as u
from astropy.stats.sigma_clipping import sigma_clip, SigmaClip, sigma_clipped_stats
from astropy.utils.exceptions import AstropyUserWarning
from astropy.utils.misc import NumpyRNGContext
from scipy import stats


def test_sigma_clip_axis_tuple_3D():
    'Test sigma clipping over a subset of axes (issue #7227).\n    '
    data = np.sin((0.78 * np.arange(27))).reshape(3, 3, 3)
    mask = np.zeros_like(data, dtype=np.bool_)
    data_t = np.rollaxis(data, 1, 0)
    mask_t = np.rollaxis(mask, 1, 0)
    for (data_plane, mask_plane) in zip(data_t, mask_t):
        mean = data_plane.mean()
        maxdev = (1.5 * data_plane.std())
        mask_plane[:] = np.logical_or((data_plane < (mean - maxdev)), (data_plane > (mean + maxdev)))
    result = sigma_clip(data, sigma=1.5, cenfunc=np.mean, maxiters=1, axis=(0, (- 1)))
    assert_equal(result.mask, mask)
