import numpy as np
from tadataka.rigid_transform import rotate_each
from tadataka.so3 import exp_so3


def image_coordinates(image_shape):
    '\n    Returns:\n        If image_shape is (m+1, n+1), returns np.ndarray of shape\n        (2, m+1 * n+1) in the form\n        [[x0, y0], [x1, y0], [x2, y0], ..., [xn, y0],\n         [x0, y1], [x1, y1], [x2, y1], ..., [xn, y1],\n         ...,\n         [x0, ym], [x1, ym], [x2, ym], ..., [xn, ym]]\n    '
    (height, width) = image_shape[0:2]
    (xs, ys) = np.meshgrid(np.arange(width), np.arange(height))
    return np.column_stack((xs.flatten(), ys.flatten()))
