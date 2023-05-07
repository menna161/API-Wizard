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


def triangulation_indices(n_keypoints):
    N = n_triangulated(n_keypoints)
    indices = np.arange(0, n_keypoints)
    np.random.shuffle(indices)
    return indices[:N]
