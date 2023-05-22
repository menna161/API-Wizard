import itertools
import numpy as np
from numpy.linalg import inv
from numpy.testing import assert_array_almost_equal, assert_almost_equal, assert_array_equal, assert_equal
from scipy.spatial.transform import Rotation
from tadataka.camera import CameraParameters
from tadataka.matrix import solve_linear, motion_matrix, inv_motion_matrix, get_rotation_translation, decompose_essential, estimate_fundamental, fundamental_to_essential, to_homogeneous, from_homogeneous, calc_relative_transform
from tadataka.projection import PerspectiveProjection
from tadataka.rigid_transform import transform
from tadataka.so3 import tangent_so3
from tests.utils import random_rotation_matrix


def test(R_true, t_true):
    S_true = tangent_so3(t_true)
    E_true = np.dot(R_true, S_true)
    (R1, R2, t1, t2) = decompose_essential(E_true)
    assert_array_almost_equal(t1, (- t2))
    assert_array_almost_equal(np.cross(np.dot(R1.T, t1), t_true), np.zeros(3))
    assert_array_almost_equal(np.cross(np.dot(R2.T, t1), t_true), np.zeros(3))
    assert_array_almost_equal(np.dot(R1.T, R1), np.identity(3))
    assert_array_almost_equal(np.dot(R2.T, R2), np.identity(3))
    assert_almost_equal(np.linalg.det(R1), 1.0)
    assert_almost_equal(np.linalg.det(R2), 1.0)
