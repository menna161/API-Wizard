import ctypes
import numpy as np
from astropy.modeling.core import FittableModel, custom_model
from scipy.integrate import quad
from scipy.integrate import dblquad


def discretize_bilinear_2D(model, x_range, y_range):
    '\n    Discretize model by performing a bilinear interpolation.\n    '
    x = np.arange((x_range[0] - 0.5), (x_range[1] + 0.5))
    y = np.arange((y_range[0] - 0.5), (y_range[1] + 0.5))
    (x, y) = np.meshgrid(x, y)
    values_intermediate_grid = model(x, y)
    values = (0.5 * (values_intermediate_grid[(1:, :)] + values_intermediate_grid[(:(- 1), :)]))
    values = (0.5 * (values[(:, 1:)] + values[(:, :(- 1))]))
    return values
