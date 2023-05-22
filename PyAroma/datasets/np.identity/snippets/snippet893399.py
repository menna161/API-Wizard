import copy
import numpy as np
from liegroups.numpy import SE2


def test_inv():
    T = SE2.exp([1, 2, 3])
    assert np.allclose(T.dot(T.inv()).as_matrix(), np.identity(3))
