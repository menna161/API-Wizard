import re
from tadataka.camera.normalizer import Normalizer
from tadataka.camera.parameters import CameraParameters
from tadataka.camera.distortion import FOV, RadTan, NoDistortion
from tadataka.decorator import allow_1d


def resize(cm, scale):
    return CameraModel(CameraParameters((cm.camera_parameters.focal_length * scale), (cm.camera_parameters.offset * scale)), cm.distortion_model)
