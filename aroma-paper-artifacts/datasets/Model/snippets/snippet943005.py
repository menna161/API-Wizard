from pathlib import Path
from numpy.testing import assert_array_equal
from tadataka.camera.distortion import FOV
from tadataka.camera.io import load, save
from tadataka.camera.model import CameraModel
from tadataka.camera.parameters import CameraParameters


def test_save():
    camera_parameters = CameraParameters(focal_length=[123.4, 200.8], offset=[250.1, 150.0])
    distortion_model = FOV(0.02)
    camera_model1 = CameraModel(camera_parameters, distortion_model)
    camera_parameters = CameraParameters(focal_length=[400.3, 500.0], offset=[248.0, 152.0])
    distortion_model = FOV((- 0.01))
    camera_model2 = CameraModel(camera_parameters, distortion_model)
    path = Path(workspace, 'camera_models.txt')
    camera_models = {1: camera_model1, 2: camera_model2}
    save(path, camera_models)
    expected = '1 FOV 123.4 200.8 250.1 150.0 0.02\n2 FOV 400.3 500.0 248.0 152.0 -0.01\n'
    with open(path, 'r') as f:
        s = f.read()
    assert (s == expected)
    path.unlink()
