from __future__ import absolute_import
import numpy as np
import scipy.ndimage as ndi
import cv2
from functools import partial
from functools import wraps
from . import Operation


def apply_core(self, x, y):
    if (x is not None):
        (h, w) = (x[0].shape[_row_axis], x[0].shape[_col_axis])
    elif (y is not None):
        (h, w) = (y[0].shape[_row_axis], y[0].shape[_col_axis])
    else:
        return (x, y)
    x_s = np.random.randint(0, ((h - self._size[0]) + 1))
    x_e = (x_s + self._size[0])
    y_s = np.random.randint(0, ((w - self._size[1]) + 1))
    y_e = (y_s + self._size[1])
    if (x is not None):
        x = [crop(x_i, x_s, x_e, y_s, y_e) for x_i in x]
    if (y is not None):
        y = [crop(y_i, x_s, x_e, y_s, y_e) for y_i in y]
    return (x, y)
