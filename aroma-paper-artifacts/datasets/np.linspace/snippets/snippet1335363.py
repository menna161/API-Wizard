import numpy as np
import pytest
from numpy.testing import assert_allclose
from astropy.stats.spatial import RipleysKEstimator
from astropy.utils.misc import NumpyRNGContext


@pytest.mark.parametrize('points, low, high', [(a, 5, 10), (b, (- 10), (- 5))])
def test_ripley_modes(points, low, high):
    Kest = RipleysKEstimator(area=25, x_max=high, y_max=high, x_min=low, y_min=low)
    r = np.linspace(0, 1.2, 25)
    Kpos_mean = np.mean(Kest.poisson(r))
    modes = ['ohser', 'translation', 'ripley']
    for m in modes:
        Kest_mean = np.mean(Kest(data=points, radii=r, mode=m))
        assert_allclose(Kpos_mean, Kest_mean, atol=0.1, rtol=0.1)
