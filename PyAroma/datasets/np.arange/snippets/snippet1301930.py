import ctypes
import numpy as np
from astropy.modeling.core import FittableModel, custom_model
from scipy.integrate import quad
from scipy.integrate import dblquad


def discretize_center_2D(model, x_range, y_range):
    '\n    Discretize model by taking the value at the center of the pixel.\n    '
    x = np.arange(*x_range)
    y = np.arange(*y_range)
    (x, y) = np.meshgrid(x, y)
    return model(x, y)
