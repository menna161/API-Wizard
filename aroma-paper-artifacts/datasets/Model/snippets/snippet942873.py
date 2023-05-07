from pathlib import Path
import numpy as np
from scipy.spatial.transform import Rotation
from skimage.io import imread
from tadataka.camera import CameraModel, CameraParameters, RadTan
from tadataka.dataset.frame import Frame
from tadataka.dataset.base import BaseDataset
from tadataka.dataset.tum import load_image_paths, synchronize
from tadataka.utils import value_list
from tadataka.pose import Pose


def get_camera_model_rgb(freiburg):
    if (freiburg == 1):
        return CameraModel(CameraParameters(focal_length=[517.3, 516.5], offset=[318.6, 255.3]), RadTan([0.2624, (- 0.9531), (- 0.0054), 0.0026, 1.1633]))
    if (freiburg == 2):
        return CameraModel(CameraParameters(focal_length=[520.9, 521.0], offset=[325.1, 249.7]), RadTan([0.2312, (- 0.7849), (- 0.0033), (- 0.0001), 0.9172]))
    if (freiburg == 3):
        return CameraModel(CameraParameters(focal_length=[535.4, 539.2], offset=[320.1, 247.6]), RadTan([0, 0, 0, 0, 0]))
    raise ValueError(no_such_sequence_message(freiburg))
