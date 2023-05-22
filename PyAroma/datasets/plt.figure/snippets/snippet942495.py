from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib
from skimage.io import imread
import numpy as np
from tadataka.camera.io import load
from tadataka.dataset.tum_rgbd import TumRgbdDataset
from tadataka.feature import extract_features, Matcher
from tadataka.plot import plot_map, plot_matches
from tadataka.pose import Pose, estimate_pose_change, solve_pnp
from tadataka.triangulation import TwoViewTriangulation
from tadataka.visual_odometry.vitamin_e import Tracker, init_keypoint_frame, get_array, match_keypoints
from tadataka.camera import RadTan, CameraParameters, CameraModel


def plot_track(image1, image2, keypoints1, keypoints2):
    matches12 = match_keypoints(keypoints1, keypoints2)
    (indices1, indices2) = (matches12[(:, 0)], matches12[(:, 1)])
    keypoints1_ = get_array(keypoints1)
    keypoints2_ = get_array(keypoints2)
    colors = np.random.random((len(matches12), 3))
    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.scatter(keypoints1_[(indices1, 0)], keypoints1_[(indices1, 1)], s=0.1, c=colors)
    ax.imshow(image1, cmap='gray')
    ax.axis('off')
    (h, w) = image1.shape[0:2]
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax = fig.add_subplot(122)
    ax.scatter(keypoints2_[(indices2, 0)], keypoints2_[(indices2, 1)], s=0.1, c=colors)
    ax.imshow(image2, cmap='gray')
    ax.axis('off')
    (h, w) = image2.shape[0:2]
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    plt.show()
