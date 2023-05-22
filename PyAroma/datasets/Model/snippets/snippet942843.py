import numpy as np
from pathlib import Path
import yaml
from skimage.io import imread
from scipy.spatial.transform import Rotation
from tadataka.dataset import tum
from tadataka.dataset.base import BaseDataset
from tadataka.dataset.frame import Frame
from tadataka.utils import value_list
from tadataka.camera.distortion import RadTan
from tadataka.camera.parameters import CameraParameters
from tadataka.camera.model import CameraModel
from tadataka.matrix import get_rotation_translation, motion_matrix
from tadataka.pose import Pose


def __init__(self, dataset_root):
    (intrinsics0, dist_coeffs0, self.T_bc0) = load_camera_params(dataset_root, 0)
    (intrinsics1, dist_coeffs1, self.T_bc1) = load_camera_params(dataset_root, 1)
    self.camera_model0 = CameraModel(CameraParameters(focal_length=intrinsics0[0:2], offset=intrinsics0[2:4]), RadTan(dist_coeffs0))
    self.camera_model1 = CameraModel(CameraParameters(focal_length=intrinsics1[0:2], offset=intrinsics1[2:4]), RadTan(dist_coeffs1))
    (timestamps0, image_paths0) = load_image_paths(dataset_root, 0)
    (timestamps1, image_paths1) = load_image_paths(dataset_root, 1)
    (timestamps_body, rotations_wb, t_wb) = load_body_poses(dataset_root)
    matches = tum.synchronize(timestamps_body, timestamps0, timestamps_ref=timestamps1)
    indices_wb = matches[(:, 0)]
    indices0 = matches[(:, 1)]
    indices1 = matches[(:, 2)]
    self.rotations_wb = value_list(rotations_wb, indices_wb)
    self.t_wb = value_list(t_wb, indices_wb)
    self.image_paths0 = value_list(image_paths0, indices0)
    self.image_paths1 = value_list(image_paths1, indices1)
    self.length = matches.shape[0]
