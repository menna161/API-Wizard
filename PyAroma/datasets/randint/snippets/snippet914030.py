from __future__ import absolute_import
import numpy as np
import scipy.ndimage as ndi
import warnings
from . import Operation
from . import image


def apply_core(self, x, y):
    if (x is not None):
        (h, w, d) = (x[0].shape[axis] for axis in (_row_axis, _col_axis, _depth_axis))
    elif (y is not None):
        (h, w, d) = (y[0].shape[axis] for axis in (_row_axis, _col_axis, _depth_axis))
    else:
        return (x, y)
    x_s = np.random.randint(0, ((h - self._size[0]) + 1))
    x_e = (x_s + self._size[0])
    y_s = np.random.randint(0, ((w - self._size[1]) + 1))
    y_e = (y_s + self._size[1])
    z_s = np.random.randint(0, ((d - self._size[2]) + 1))
    z_e = (z_s + self._size[2])
    if (x is not None):
        x = [crop(x_i, x_s, x_e, y_s, y_e, z_s, z_e) for x_i in x]
    if (y is not None):
        y = [crop(y_i, x_s, x_e, y_s, y_e, z_s, z_e) for y_i in y]
    return (x, y)
