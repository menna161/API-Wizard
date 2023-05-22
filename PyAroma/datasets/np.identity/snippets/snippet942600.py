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


def select_valid_pose(R1A, R1B, t1a, t1b, keypoints0, keypoints1):
    (R0, t0) = (np.identity(3), np.zeros(3))
    n_max_valid_depth = (- 1)
    (argmax_R, argmax_t, argmax_depth_mask) = (None, None, None)
    indices = triangulation_indices(min(100, len(keypoints0)))
    keypoints = np.stack((keypoints0[indices], keypoints1[indices]))
    for (i, (R_, t_)) in enumerate(itertools.product((R1A, R1B), (t1a, t1b))):
        (_, depths) = linear_triangulation(np.array([R0, R_]), np.array([t0, t_]), keypoints)
        depth_mask = compute_depth_mask(depths)
        n_valid_depth = np.sum(depth_mask)
        if (n_valid_depth > n_max_valid_depth):
            n_max_valid_depth = n_valid_depth
            (argmax_R, argmax_t, argmax_depth_mask) = (R_, t_, depth_mask)
    if (not depth_condition(argmax_depth_mask)):
        warn_points_behind_cameras()
    return (argmax_R, argmax_t)
