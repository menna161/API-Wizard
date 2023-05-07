import numpy as np
from skimage.color import rgb2gray
from skimage.transform import resize
from tadataka.warp import warp2d, Warp2D
from tadataka.camera import CameraModel
from tadataka.matrix import inv_motion_matrix
from tadataka.pose import Pose, estimate_pose_change
from tadataka import camera
from tadataka.vo.dvo import PoseChangeEstimator
from tadataka.feature import extract_features, Matcher
from tadataka.dataset import NewTsukubaDataset, TumRgbdDataset
from tadataka.vo.semi_dense.regularization import regularize
from tadataka.vo.semi_dense.hypothesis import HypothesisMap
from tadataka.vo.semi_dense.fusion import fusion
from tadataka.camera.normalizer import Normalizer
from tadataka.numeric import safe_invert
from tadataka.vo.semi_dense.semi_dense import InvDepthEstimator, InvDepthMapEstimator
from tadataka.vo.semi_dense.reference import make_reference_selector
from rust_bindings.semi_dense import increment_age, propagate, update_depth, Frame, Params
from rust_bindings.camera import CameraParameters
from rust_bindings.semi_dense import estimate_debug_
from examples.plot import plot_depth
from tests.dataset.path import new_tsukuba


def dvo(camera_params0, camera_params1, image0, image1, depth_map0, variance_map0):
    estimator = PoseChangeEstimator(CameraModel(camera_params0, distortion_model=None), CameraModel(camera_params1, distortion_model=None), n_coarse_to_fine=7)
    weights = safe_invert(variance_map0)
    pose10 = estimator(image0, depth_map0, image1, weights)
    return pose10.T
