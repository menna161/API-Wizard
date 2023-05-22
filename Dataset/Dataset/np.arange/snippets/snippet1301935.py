import ctypes
import numpy as np
from astropy.modeling.core import FittableModel, custom_model
from scipy.integrate import quad
from scipy.integrate import dblquad


def discretize_integrate_1D(model, x_range):
    '\n    Discretize model by integrating numerically the model over the bin.\n    '
    from scipy.integrate import quad
    x = np.arange((x_range[0] - 0.5), (x_range[1] + 0.5))
    values = np.array([])
    for i in range((x.size - 1)):
        values = np.append(values, quad(model, x[i], x[(i + 1)])[0])
    return values
