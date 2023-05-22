import ctypes
import numpy as np
from astropy.modeling.core import FittableModel, custom_model
from scipy.integrate import quad
from scipy.integrate import dblquad


def discretize_center_1D(model, x_range):
    '\n    Discretize model by taking the value at the center of the bin.\n    '
    x = np.arange(*x_range)
    return model(x)
