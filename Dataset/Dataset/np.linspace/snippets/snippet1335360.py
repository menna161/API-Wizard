import numpy as np
import pytest
from numpy.testing import assert_allclose
from astropy.stats.spatial import RipleysKEstimator
from astropy.utils.misc import NumpyRNGContext


@pytest.mark.parametrize('points, x_min, x_max', [(a, 0, 10), (b, (- 5), 5)])
def test_ripley_K_implementation(points, x_min, x_max):
    "\n    Test against Ripley's K function implemented in R package `spatstat`\n        +-+---------+---------+----------+---------+-+\n      6 +                                          * +\n        |                                            |\n        |                                            |\n    5.5 +                                            +\n        |                                            |\n        |                                            |\n      5 +                     *                      +\n        |                                            |\n    4.5 +                                            +\n        |                                            |\n        |                                            |\n      4 + *                                          +\n        +-+---------+---------+----------+---------+-+\n          1        1.5        2         2.5        3\n\n        +-+---------+---------+----------+---------+-+\n      3 + *                                          +\n        |                                            |\n        |                                            |\n    2.5 +                                            +\n        |                                            |\n        |                                            |\n      2 +                     *                      +\n        |                                            |\n    1.5 +                                            +\n        |                                            |\n        |                                            |\n      1 +                                          * +\n        +-+---------+---------+----------+---------+-+\n         -3       -2.5       -2        -1.5       -1\n    "
    area = 100
    r = np.linspace(0, 2.5, 5)
    Kest = RipleysKEstimator(area=area, x_min=x_min, y_min=x_min, x_max=x_max, y_max=x_max)
    ANS_NONE = np.array([0, 0, 0, 66.667, 66.667])
    assert_allclose(ANS_NONE, Kest(data=points, radii=r, mode='none'), atol=0.001)
    ANS_TRANS = np.array([0, 0, 0, 82.304, 82.304])
    assert_allclose(ANS_TRANS, Kest(data=points, radii=r, mode='translation'), atol=0.001)
