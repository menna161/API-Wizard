import copy
import numpy as np
from liegroups.numpy import SO3


def test_left_jacobians():
    phi_small = [0.0, 0.0, 0.0]
    phi_big = [(np.pi / 2), (np.pi / 3), (np.pi / 4)]
    left_jacobian_small = SO3.left_jacobian(phi_small)
    inv_left_jacobian_small = SO3.inv_left_jacobian(phi_small)
    assert np.allclose(left_jacobian_small.dot(inv_left_jacobian_small), np.identity(3))
    left_jacobian_big = SO3.left_jacobian(phi_big)
    inv_left_jacobian_big = SO3.inv_left_jacobian(phi_big)
    assert np.allclose(left_jacobian_big.dot(inv_left_jacobian_big), np.identity(3))
