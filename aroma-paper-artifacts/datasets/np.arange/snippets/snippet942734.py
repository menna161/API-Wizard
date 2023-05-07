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


def test_eq():
    rotaiton0 = Rotation.from_matrix(random_rotation_matrix(3))
    rotaiton1 = Rotation.from_matrix(random_rotation_matrix(3))
    t0 = np.zeros(3)
    t1 = np.arange(3)
    assert (Pose(rotaiton0, t0) == Pose(rotaiton0, t0))
    assert (Pose(rotaiton1, t1) == Pose(rotaiton1, t1))
    assert (Pose(rotaiton0, t0) != Pose(rotaiton0, t1))
    assert (Pose(rotaiton0, t0) != Pose(rotaiton1, t0))
    assert (Pose(rotaiton0, t0) != Pose(rotaiton1, t1))
