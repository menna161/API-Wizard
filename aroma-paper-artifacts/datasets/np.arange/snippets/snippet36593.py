import pickle
import numpy as np
from numpy.testing import assert_almost_equal, assert_array_equal, assert_equal
from modl.utils.randomkit import RandomState


def test_shuffle_with_trace():
    ind = np.arange(10)
    ind2 = np.arange(9, (- 1), (- 1))
    rs = RandomState(seed=0)
    perm = rs.shuffle_with_trace([ind, ind2])
    assert_array_equal(ind, [2, 8, 4, 9, 1, 6, 7, 3, 0, 5])
    assert_array_equal(ind2, [7, 1, 5, 0, 8, 3, 2, 6, 9, 4])
    assert_array_equal(ind, perm)
