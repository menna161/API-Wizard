import copy
import numpy as np
from liegroups.numpy import SE3


def test_inv():
    T = SE3.exp([1, 2, 3, 4, 5, 6])
    assert np.allclose(T.dot(T.inv()).as_matrix(), np.identity(4))
