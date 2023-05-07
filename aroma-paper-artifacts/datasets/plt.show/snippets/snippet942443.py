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


def dense_mvs(frames):
    features = [extract_features(f.image) for f in frames]
    trackers = []
    for i in range((len(frames) - 1)):
        (features0, features1) = (features[i], features[(i + 1)])
        matches01 = match(features0, features1)
        tracker = Tracker(features0.keypoints[matches01[(:, 0)]], features1.keypoints[matches01[(:, 1)]], frames[(i + 1)].image)
        trackers.append(tracker)
    dense_keypoints0 = extract_curvature_extrema(frames[0].image)
    dense_keypoints = track(trackers, dense_keypoints0)
    fig = plt.figure()
    for i in range(len(frames)):
        ax = fig.add_subplot(1, len(frames), (i + 1))
        ax.imshow(frames[i].image)
        ax.scatter(dense_keypoints[(:, i, 0)], dense_keypoints[(:, i, 1)], s=0.1, c='red')
    plt.show()
    dense_keypoints = undistort([f.camera_model for f in frames], dense_keypoints)
    poses = [Pose(f.rotation, f.position).world_to_local() for f in frames]
    (points, depths) = Triangulation(poses).triangulate(dense_keypoints)
    return (poses, points, dense_keypoints)
