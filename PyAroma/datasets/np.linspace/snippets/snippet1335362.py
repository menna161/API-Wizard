import numpy as np
import pytest
from numpy.testing import assert_allclose
from astropy.stats.spatial import RipleysKEstimator
from astropy.utils.misc import NumpyRNGContext


@pytest.mark.parametrize('points, low, high', [(a, 0, 1), (b, (- 1), 0)])
def test_ripley_large_density(points, low, high):
    Kest = RipleysKEstimator(area=1, x_min=low, x_max=high, y_min=low, y_max=high)
    r = np.linspace(0, 0.25, 25)
    Kpos = Kest.poisson(r)
    modes = ['ohser', 'translation', 'ripley']
    for m in modes:
        Kest_r = Kest(data=points, radii=r, mode=m)
        assert_allclose(Kpos, Kest_r, atol=0.1)
