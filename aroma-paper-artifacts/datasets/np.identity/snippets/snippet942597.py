import itertools
import numpy as np
from scipy.spatial.transform import Rotation
import cv2
from tadataka.depth import depth_condition, warn_points_behind_cameras, compute_depth_mask
from tadataka.exceptions import NotEnoughInliersException
from tadataka.matrix import estimate_fundamental, decompose_essential, motion_matrix
from tadataka.so3 import exp_so3, log_so3
from tadataka.se3 import exp_se3_t_
from tadataka.triangulation import linear_triangulation


def solve_pnp(points, keypoints):
    assert (points.shape[0] == keypoints.shape[0])
    if (keypoints.shape[0] < min_correspondences):
        raise NotEnoughInliersException('No sufficient correspondences')
    t = calc_reprojection_threshold(keypoints, k=3.0)
    (retval, omega, t, inliers) = cv2.solvePnPRansac(points.astype(np.float64), keypoints.astype(np.float64), np.identity(3), np.zeros(4), reprojectionError=t, flags=cv2.SOLVEPNP_EPNP)
    if (not retval):
        raise RuntimeError('Pose estimation failed')
    if (len(inliers.flatten()) == 0):
        raise NotEnoughInliersException('No inliers found')
    return Pose(Rotation.from_rotvec(omega.flatten()), t.flatten())
