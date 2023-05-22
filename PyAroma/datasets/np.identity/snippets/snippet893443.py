import copy
import numpy as np
from liegroups.numpy import SO3


def test_inv():
    C = SO3.exp(((np.pi * np.ones(3)) / 4))
    assert np.allclose(C.dot(C.inv()).mat, np.identity(3))
