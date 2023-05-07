import pytest
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_equal
from scipy.spatial.transform import Rotation
from tadataka.projection import pi
from tadataka.so3 import exp_so3
from tadataka.camera import CameraParameters
from tadataka.exceptions import NotEnoughInliersException
from tadataka.dataset.observations import generate_translations
from tadataka.pose import estimate_pose_change, n_triangulated, solve_pnp, triangulation_indices, Pose
from tadataka.rigid_transform import transform
from tests.utils import random_rotation_matrix


def test_R():
    pose = Pose(Rotation.from_rotvec(np.zeros(3)), np.zeros(3))
    assert_array_almost_equal(pose.R, np.identity(3))
    (rotvec, t) = (np.array([np.pi, 0, 0]), np.zeros(3))
    pose = Pose(Rotation.from_rotvec(rotvec), t)
    assert_array_almost_equal(pose.R, np.diag([1, (- 1), (- 1)]))
