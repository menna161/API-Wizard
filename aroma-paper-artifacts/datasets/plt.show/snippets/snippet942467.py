import numpy as np
from skimage.color import rgb2gray, gray2rgb
from skimage.transform import resize
from tqdm import tqdm
from tadataka.camera import CameraModel
from tadataka.rigid_motion import LeastSquaresRigidMotion
from tadataka.vo.semi_dense.frame_selection import ReferenceSelector
from tadataka.coordinates import image_coordinates
from tadataka.dataset import TumRgbdDataset
from tadataka.vo.semi_dense.frame import Frame
from tadataka.vo.semi_dense.age import increment_age
from tadataka.vo.semi_dense.common import invert_depth
from tadataka.feature import extract_features, Matcher
from tadataka.vo.semi_dense.flag import ResultFlag as FLAG
from tadataka.vo.semi_dense.fusion import fusion
from tadataka.vo.semi_dense.propagation import propagate
from tadataka.pose import WorldPose, estimate_pose_change
from tadataka.vo.dvo import PoseChangeEstimator
from tadataka.matrix import to_homogeneous
from tadataka.warp import Warp2D
from tadataka.rigid_transform import transform, Transform
from tadataka.dataset import NewTsukubaDataset
from tests.dataset.path import new_tsukuba
from examples.plot import plot_depth, plot_prior
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
from tadataka.vo.semi_dense.semi_dense import InverseDepthMapEstimator
from tadataka.camera import CameraParameters
from tadataka.plot import plot_matches
from tadataka.triangulation import TwoViewTriangulation
from tadataka.plot import plot_map


def main_():
    dataset = TumRgbdDataset('datasets/rgbd_dataset_freiburg1_desk', which_freiburg=1)
    frames = dataset[0:200:10]
    inv_depth_map = invert_depth(frames[0].depth_map)
    variance_map = (10.0 * np.ones(frames[0].depth_map.shape))
    trajectory_true = []
    trajectory_pred = []
    for i in range(len(frames)):
        (camera_model, pose_true, image, depth_map_true) = frames[i]
        Frame(camera_model, image, pose_pred)
        pose10_true = (frame1_.pose.inv() * frame0_.pose)
        pose_true = (pose10_true * pose_true)
        trajectory_pred.append(pose_pred.t)
        trajectory_true.append(pose_true.t)
    trajectory_true = np.array(trajectory_true)
    trajectory_pred = np.array(trajectory_pred)
    (R, t, s) = LeastSquaresRigidMotion(trajectory_pred, trajectory_true).solve()
    trajectory_pred = Transform(R, t, s)(trajectory_pred)
    print('MSE: ', np.power((trajectory_pred - trajectory_true), 2).mean())
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(trajectory_pred[(:, 0)], trajectory_pred[(:, 1)], trajectory_pred[(:, 2)], label='pred')
    ax.plot(trajectory_true[(:, 0)], trajectory_true[(:, 1)], trajectory_true[(:, 2)], label='true')
    plt.legend()
    plt.show()
