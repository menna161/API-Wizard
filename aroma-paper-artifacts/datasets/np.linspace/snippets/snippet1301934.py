import ctypes
import numpy as np
from astropy.modeling.core import FittableModel, custom_model
from scipy.integrate import quad
from scipy.integrate import dblquad


def discretize_oversample_2D(model, x_range, y_range, factor=10):
    '\n    Discretize model by taking the average on an oversampled grid.\n    '
    x = np.linspace((x_range[0] - (0.5 * (1 - (1 / factor)))), (x_range[1] - (0.5 * (1 + (1 / factor)))), num=((x_range[1] - x_range[0]) * factor))
    y = np.linspace((y_range[0] - (0.5 * (1 - (1 / factor)))), (y_range[1] - (0.5 * (1 + (1 / factor)))), num=((y_range[1] - y_range[0]) * factor))
    (x_grid, y_grid) = np.meshgrid(x, y)
    values = model(x_grid, y_grid)
    shape = ((y.size // factor), factor, (x.size // factor), factor)
    values = np.reshape(values, shape)
    return values.mean(axis=3).mean(axis=1)
