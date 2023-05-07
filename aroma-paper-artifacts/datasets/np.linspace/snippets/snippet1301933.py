import ctypes
import numpy as np
from astropy.modeling.core import FittableModel, custom_model
from scipy.integrate import quad
from scipy.integrate import dblquad


def discretize_oversample_1D(model, x_range, factor=10):
    '\n    Discretize model by taking the average on an oversampled grid.\n    '
    x = np.linspace((x_range[0] - (0.5 * (1 - (1 / factor)))), (x_range[1] - (0.5 * (1 + (1 / factor)))), num=((x_range[1] - x_range[0]) * factor))
    values = model(x)
    values = np.reshape(values, ((x.size // factor), factor))
    return values.mean(axis=1)
