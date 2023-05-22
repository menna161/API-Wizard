import numpy as np
import pytest
from numpy.testing import assert_allclose
from astropy.stats.spatial import RipleysKEstimator
from astropy.utils.misc import NumpyRNGContext


@pytest.mark.parametrize('points', [a, b])
def test_ripley_uniform_property(points):
    area = 50
    Kest = RipleysKEstimator(area=area)
    r = np.linspace(0, 20, 5)
    assert_allclose(area, Kest(data=points, radii=r, mode='none')[4])
