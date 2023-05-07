import numpy as np
from numpy.testing import assert_array_almost_equal
from scipy.spatial.transform import Rotation
from tadataka.camera import CameraModel, CameraParameters
from tadataka.warp import warp_depth, Warp2D, Warp3D, warp2d_, LocalWarp2D
from tadataka.pose import Pose


def test_warp2d():
    rotation = Rotation.from_rotvec([0, (np.pi / 2), 0])
    t_w0 = np.array([0, 0, 3])
    pose_w0 = Pose(rotation, t_w0)
    t_w1 = np.array([0, 0, 4])
    pose_w1 = Pose(rotation, t_w1)
    warp3d = Warp3D(pose_w0, pose_w1)
    xs0 = np.array([[0, 0], [0, (- 1)]], dtype=np.float64)
    depths0 = np.array([2, 4], dtype=np.float64)
    (xs1, depths1) = warp_depth(warp3d, xs0, depths0)
    assert_array_almost_equal(xs1, [[0.5, 0], [0.25, (- 1)]])
    assert_array_almost_equal(depths1, [2, 4])
    camera_model0 = CameraModel(CameraParameters(focal_length=[2, 2], offset=[0, 0]), distortion_model=None)
    camera_model1 = CameraModel(CameraParameters(focal_length=[3, 3], offset=[0, 0]), distortion_model=None)
    us0 = (2.0 * xs0)
    warp2d = Warp2D(camera_model0, camera_model1, pose_w0, pose_w1)
    (us1, depths1) = warp2d(us0, depths0)
    assert_array_almost_equal(us1, (3.0 * xs1))
