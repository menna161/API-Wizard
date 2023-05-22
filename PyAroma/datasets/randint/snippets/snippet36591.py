import pickle
import numpy as np
from numpy.testing import assert_almost_equal, assert_array_equal, assert_equal
from modl.utils.randomkit import RandomState


def test_random():
    rs = RandomState(seed=0)
    vals = [rs.randint(10) for t in range(10000)]
    assert_almost_equal(np.mean(vals), 5.018)
    vals = [rs.binomial(1000, 0.8) for t in range(10000)]
    assert_almost_equal(np.mean(vals), 799.8564)
