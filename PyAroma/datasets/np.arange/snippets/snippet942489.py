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


def choose_nonoverlap(size, ratio):
    N = int((size * ratio))
    indices_ = np.arange(0, size)
    np.random.shuffle(indices_)
    indices = indices_[:N]
    return indices
