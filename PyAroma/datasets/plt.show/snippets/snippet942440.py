from pathlib import Path
import numpy as np
from skimage.color import rgb2gray
from skimage.feature import BRIEF
from matplotlib import pyplot as plt
from tadataka.camera import CameraModel, CameraParameters, FOV
from tadataka.coordinates import yx_to_xy, xy_to_yx
from tadataka.dataset.new_tsukuba import NewTsukubaDataset
from tadataka.feature import extract_features, Features, Matcher
from tadataka.triangulation import Triangulation
from tadataka.flow_estimation.extrema_tracker import ExtremaTracker
from tadataka.flow_estimation.image_curvature import extract_curvature_extrema
from tadataka.flow_estimation.image_curvature import compute_image_curvature
from tadataka.flow_estimation.flow_estimation import estimate_affine_transform
from tadataka.plot import plot_map, plot_matches
from tadataka.pose import Pose
from tadataka.triangulation import TwoViewTriangulation
from tadataka.utils import is_in_image_range
from matplotlib import rcParams
from tadataka.dataset.tum_rgbd import TumRgbdDataset
from tadataka.local_ba import run_ba


def dense_track_triangulation(frame0, frame1):
    features0 = extract_dense_features(image0)
    features1 = extract_dense_features(image1)
    matches01 = match(features0, features1)
    affine = estimate_affine_transform(features0.keypoints[matches01[(:, 0)]], features1.keypoints[matches01[(:, 1)]])
    dense_keypoints0 = extract_curvature_extrema(image0)
    dense_keypoints1 = affine.transform(dense_keypoints0)
    mask = is_in_image_range(dense_keypoints1, image1.shape)
    et = ExtremaTracker(compute_image_curvature(rgb2gray(image1)), lambda_=10.0)
    dense_keypoints1[mask] = et.optimize(dense_keypoints1[mask])
    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.imshow(image0)
    ax.scatter(dense_keypoints0[(mask, 0)], dense_keypoints0[(mask, 1)], s=0.1, c='red')
    ax = fig.add_subplot(122)
    ax.imshow(image1)
    ax.scatter(dense_keypoints1[(mask, 0)], dense_keypoints1[(mask, 1)], s=0.1, c='red')
    plt.show()
    (points, depth_mask) = TwoViewTriangulation(pose0, pose1).triangulate(frame0.camera_model.undistort(dense_keypoints0[mask]), frame1.camera_model.undistort(dense_keypoints1[mask]))
    plot_map([pose0, pose1], points)
