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


def to_perspective(camera_model):
    return CameraModel(camera_model.camera_parameters, distortion_model=None)
