import ctypes
import numpy as np
from astropy.modeling.core import FittableModel, custom_model
from scipy.integrate import quad
from scipy.integrate import dblquad


def discretize_linear_1D(model, x_range):
    '\n    Discretize model by performing a linear interpolation.\n    '
    x = np.arange((x_range[0] - 0.5), (x_range[1] + 0.5))
    values_intermediate_grid = model(x)
    return (0.5 * (values_intermediate_grid[1:] + values_intermediate_grid[:(- 1)]))
