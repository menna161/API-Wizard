import pickle
import numpy as np
from numpy.testing import assert_almost_equal, assert_array_equal, assert_equal
from modl.utils.randomkit import RandomState


def test_shuffle():
    ind = np.arange(10)
    rs = RandomState(seed=0)
    rs.shuffle(ind)
    assert_array_equal(ind, [2, 8, 4, 9, 1, 6, 7, 3, 0, 5])
