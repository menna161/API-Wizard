from __future__ import absolute_import
import numpy as np
import scipy.ndimage as ndi
import cv2
from functools import partial
from functools import wraps
from . import Operation


def apply_core(self, x, y):
    size = (np.random.randint(self._size[0], (self._resize_size[0] + 1)), np.random.randint(self._size[1], (self._resize_size[1] + 1)))
    if (x is not None):
        x = [resize(x_i, size, self._interp_order[0]) for x_i in x]
    if (y is not None):
        y = [resize(y_i, size, self._interp_order[1]) for y_i in y]
    return super().apply_core(x, y)
