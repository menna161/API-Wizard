import numpy as np
from numpy.testing import assert_array_almost_equal
from scipy.spatial.transform import Rotation
from tadataka.camera import CameraModel, CameraParameters
from tadataka.warp import warp_depth, Warp2D, Warp3D, warp2d_, LocalWarp2D
from tadataka.pose import Pose


def test_warp2d_():
    rotation = Rotation.from_rotvec([0, (np.pi / 2), 0])
    t = np.array([0, 0, 4])
    pose10 = Pose(rotation, t)
    xs0 = np.array([[0, 0], [2, (- 1)]], dtype=np.float64)
    depths0 = np.array([2, 4], dtype=np.float64)
    (xs1, depths1) = warp2d_(pose10.T, xs0, depths0)
    assert_array_almost_equal(xs1, [[0.5, 0.0], [(- 1.0), 1.0]])
    assert_array_almost_equal(depths1, [4.0, (- 4.0)])
    camera_model0 = CameraModel(CameraParameters(focal_length=[2, 2], offset=[0, 0]), distortion_model=None)
    camera_model1 = CameraModel(CameraParameters(focal_length=[3, 3], offset=[0, 0]), distortion_model=None)
    warp2d = LocalWarp2D(camera_model0, camera_model1, pose10)
    us0 = (2.0 * xs0)
    (us1, depths1) = warp2d(us0, depths0)
    assert_array_almost_equal(us1, (3.0 * xs1))
