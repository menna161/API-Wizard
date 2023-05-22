import pickle
import numpy as np
from numpy.testing import assert_almost_equal, assert_array_equal, assert_equal
from modl.utils.randomkit import RandomState


def test_random_state_pickle():
    rs = RandomState(seed=0)
    random_integer = rs.randint(5)
    pickle_rs = pickle.dumps(rs)
    pickle_rs = pickle.loads(pickle_rs)
    pickle_random_integer = pickle_rs.randint(5)
    assert_equal(random_integer, pickle_random_integer)
