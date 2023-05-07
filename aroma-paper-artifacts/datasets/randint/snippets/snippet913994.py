from __future__ import absolute_import
import numpy as np
import scipy.ndimage as ndi
import cv2
from functools import partial
from functools import wraps
from . import Operation


@clip
def pepper_noise(x, ratio, cval=None):
    if (cval is None):
        cval = np.min(x)
    n_sample = int(np.ceil((x.size * ratio)))
    indices = [np.random.randint(0, s, n_sample) for s in x.shape]
    x[tuple(indices)] = cval
    return x
