import re
from tadataka.camera.normalizer import Normalizer
from tadataka.camera.parameters import CameraParameters
from tadataka.camera.distortion import FOV, RadTan, NoDistortion
from tadataka.decorator import allow_1d


def parse_(string):
    params = re.split('\\s+', string)
    distortion_type = params[0]
    params = [float(v) for v in params[1:]]
    camera_parameters = CameraParameters.from_params(params[0:4])
    dist_params = params[4:]
    if (distortion_type == 'FOV'):
        distortion_model = FOV.from_params(dist_params)
    elif (distortion_type == 'RadTan'):
        distortion_model = RadTan.from_params(dist_params)
    else:
        ValueError(('Unknown distortion model: ' + distortion_type))
    return CameraModel(camera_parameters, distortion_model)
