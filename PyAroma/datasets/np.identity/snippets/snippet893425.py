import copy
import numpy as np
from liegroups.numpy import SO2


def test_inv():
    C = SO2.exp((np.pi / 4))
    assert np.allclose(C.dot(C.inv()).mat, np.identity(2))
