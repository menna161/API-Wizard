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


def get_camera_model_depth(freiburg):
    if (freiburg == 1):
        return CameraModel(CameraParameters(focal_length=[591.1, 590.1], offset=[331.0, 234.0]), RadTan([(- 0.041), 0.3286, 0.0087, 0.0051, (- 0.5643)]))
    if (freiburg == 2):
        return CameraModel(CameraParameters(focal_length=[580.8, 581.8], offset=[308.8, 253.0]), RadTan([(- 0.2297), 1.4766, 0.0005, (- 0.0075), (- 3.4194)]))
    if (freiburg == 3):
        return CameraModel(CameraParameters(focal_length=[567.6, 570.2], offset=[324.7, 250.1]), RadTan([0, 0, 0, 0, 0]))
    raise ValueError(no_such_sequence_message(freiburg))
