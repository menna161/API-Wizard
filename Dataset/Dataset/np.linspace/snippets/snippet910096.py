import packaging
import packaging.version
import collections
import numpy as np
import scipy.ndimage.filters
import matplotlib
import matplotlib.scale
import matplotlib.transforms
import matplotlib.ticker
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.font_manager import FontProperties
import warnings


def __init__(self, transform, smin, smax, resolution=1000):
    matplotlib.transforms.Transform.__init__(self)
    self._transform = transform
    self._s_range = np.linspace(smin, smax, resolution)
    self._x_range = transform.transform_non_affine(self._s_range)
    self._xmin = transform.transform_non_affine(smin)
    self._xmax = transform.transform_non_affine(smax)
    if (self._xmin > self._xmax):
        (self._xmax, self._xmin) = (self._xmin, self._xmax)
