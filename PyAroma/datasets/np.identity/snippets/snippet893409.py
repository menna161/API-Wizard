import copy
import numpy as np
from liegroups.numpy import SE3


def test_left_jacobian():
    xi1 = [1, 2, 3, 4, 5, 6]
    assert np.allclose(SE3.left_jacobian(xi1).dot(SE3.inv_left_jacobian(xi1)), np.identity(6))
    xi2 = [0, 0, 0, 0, 0, 0]
    assert np.allclose(SE3.left_jacobian(xi2).dot(SE3.inv_left_jacobian(xi2)), np.identity(6))
