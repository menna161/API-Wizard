import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
from tadataka.camera import CameraModel, CameraParameters, FOV, resize


def test_resize():
    distortion_model = FOV(0.02)
    camera_model = CameraModel(CameraParameters(focal_length=[40, 48], offset=[20, 16]), distortion_model=distortion_model)
    resized = resize(camera_model, (1 / 4))
    assert_array_almost_equal(resized.camera_parameters.focal_length, [10, 12])
    assert_array_almost_equal(resized.camera_parameters.offset, [5, 4])
    assert (resized.distortion_model is distortion_model)
