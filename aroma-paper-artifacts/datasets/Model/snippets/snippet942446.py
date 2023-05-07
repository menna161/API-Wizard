from skimage.color import rgb2gray
from skimage.transform import rescale
from tqdm import tqdm
from tadataka.metric import PhotometricError
from tadataka.pose import WorldPose
from tadataka.dataset import TumRgbdDataset, NewTsukubaDataset
from tadataka.vo.dvo import PoseChangeEstimator
from tadataka.camera import CameraModel
from tadataka import camera
from tests.dataset.path import new_tsukuba
from examples.plot import plot_trajectory, plot_warp
import numpy as np
from examples.plot import plot_warp


def to_perspective(camera_model):
    return CameraModel(camera_model.camera_parameters, distortion_model=None)
