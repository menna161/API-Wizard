from pathlib import Path
from skimage.io import imread
import numpy as np
from matplotlib import pyplot as plt
from tadataka.camera.io import load
from tadataka.feature import extract_features, Matcher
from tadataka.pose import Pose, estimate_pose_change, solve_pnp
from tadataka.triangulation import TwoViewTriangulation, Triangulation
from tadataka.vo.vitamin_e import Tracker, estimate_flow, get_array, init_keypoint_frame, match_keypoints, match_multiple_keypoints
from tadataka.dataset.tum_rgbd import TumRgbdDataset
from tadataka.dataset.euroc import EurocDataset
from tadataka.utils import is_in_image_range
from tadataka.plot import plot_map, plot_matches


def triangulate(camera_model0, camera_model1, pose0, pose1, keypoints0, keypoints1):
    matches01 = match_keypoints(keypoints0, keypoints1)
    keypoints0_ = get_array(keypoints0)[matches01[(:, 0)]]
    keypoints1_ = get_array(keypoints1)[matches01[(:, 1)]]
    triangulator = TwoViewTriangulation(pose0, pose1)
    A0 = camera_model0.normalize(keypoints0_)
    A1 = camera_model1.normalize(keypoints1_)
    colors = np.random.random((len(matches01), 3))
    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.scatter(A0[(:, 0)], A0[(:, 1)], s=0.1, c=colors)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax = fig.add_subplot(122)
    ax.scatter(A1[(:, 0)], A1[(:, 1)], s=0.1, c=colors)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    plt.show()
    (points01, depths) = triangulator.triangulate(camera_model0.normalize(keypoints0_), camera_model1.normalize(keypoints1_))
    return (points01, depths)
