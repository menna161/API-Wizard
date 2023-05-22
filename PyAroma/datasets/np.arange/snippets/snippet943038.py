import numpy as np
from numpy.testing import assert_array_equal
from tadataka.flow_estimation.image_curvature import compute_curvature, compute_image_curvature


def test_compute_image_curvature():
    A = np.arange(49).reshape(7, 7)
    G = compute_image_curvature(A)
    assert_array_equal(G[(2:5, 2:5)], 0)
