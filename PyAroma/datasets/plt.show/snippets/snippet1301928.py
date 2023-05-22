import ctypes
import numpy as np
from astropy.modeling.core import FittableModel, custom_model
from scipy.integrate import quad
from scipy.integrate import dblquad


def discretize_model(model, x_range, y_range=None, mode='center', factor=10):
    "\n    Function to evaluate analytical model functions on a grid.\n\n    So far the function can only deal with pixel coordinates.\n\n    Parameters\n    ----------\n    model : `~astropy.modeling.FittableModel` or callable.\n        Analytic model function to be discretized. Callables, which are not an\n        instances of `~astropy.modeling.FittableModel` are passed to\n        `~astropy.modeling.custom_model` and then evaluated.\n    x_range : tuple\n        x range in which the model is evaluated. The difference between the\n        upper an lower limit must be a whole number, so that the output array\n        size is well defined.\n    y_range : tuple, optional\n        y range in which the model is evaluated. The difference between the\n        upper an lower limit must be a whole number, so that the output array\n        size is well defined. Necessary only for 2D models.\n    mode : str, optional\n        One of the following modes:\n            * ``'center'`` (default)\n                Discretize model by taking the value\n                at the center of the bin.\n            * ``'linear_interp'``\n                Discretize model by linearly interpolating\n                between the values at the corners of the bin.\n                For 2D models interpolation is bilinear.\n            * ``'oversample'``\n                Discretize model by taking the average\n                on an oversampled grid.\n            * ``'integrate'``\n                Discretize model by integrating the model\n                over the bin using `scipy.integrate.quad`.\n                Very slow.\n    factor : float or int\n        Factor of oversampling. Default = 10.\n\n    Returns\n    -------\n    array : `numpy.array`\n        Model value array\n\n    Notes\n    -----\n    The ``oversample`` mode allows to conserve the integral on a subpixel\n    scale. Here is the example of a normalized Gaussian1D:\n\n    .. plot::\n        :include-source:\n\n        import matplotlib.pyplot as plt\n        import numpy as np\n        from astropy.modeling.models import Gaussian1D\n        from astropy.convolution.utils import discretize_model\n        gauss_1D = Gaussian1D(1 / (0.5 * np.sqrt(2 * np.pi)), 0, 0.5)\n        y_center = discretize_model(gauss_1D, (-2, 3), mode='center')\n        y_corner = discretize_model(gauss_1D, (-2, 3), mode='linear_interp')\n        y_oversample = discretize_model(gauss_1D, (-2, 3), mode='oversample')\n        plt.plot(y_center, label='center sum = {0:3f}'.format(y_center.sum()))\n        plt.plot(y_corner, label='linear_interp sum = {0:3f}'.format(y_corner.sum()))\n        plt.plot(y_oversample, label='oversample sum = {0:3f}'.format(y_oversample.sum()))\n        plt.xlabel('pixels')\n        plt.ylabel('value')\n        plt.legend()\n        plt.show()\n\n\n    "
    if (not callable(model)):
        raise TypeError('Model must be callable.')
    if (not isinstance(model, FittableModel)):
        model = custom_model(model)()
    ndim = model.n_inputs
    if (ndim > 2):
        raise ValueError('discretize_model only supports 1-d and 2-d models.')
    if (not float(np.diff(x_range)).is_integer()):
        raise ValueError("The difference between the upper an lower limit of 'x_range' must be a whole number.")
    if y_range:
        if (not float(np.diff(y_range)).is_integer()):
            raise ValueError("The difference between the upper an lower limit of 'y_range' must be a whole number.")
    if ((ndim == 2) and (y_range is None)):
        raise ValueError('y range not specified, but model is 2-d')
    if ((ndim == 1) and (y_range is not None)):
        raise ValueError('y range specified, but model is only 1-d.')
    if (mode == 'center'):
        if (ndim == 1):
            return discretize_center_1D(model, x_range)
        elif (ndim == 2):
            return discretize_center_2D(model, x_range, y_range)
    elif (mode == 'linear_interp'):
        if (ndim == 1):
            return discretize_linear_1D(model, x_range)
        if (ndim == 2):
            return discretize_bilinear_2D(model, x_range, y_range)
    elif (mode == 'oversample'):
        if (ndim == 1):
            return discretize_oversample_1D(model, x_range, factor)
        if (ndim == 2):
            return discretize_oversample_2D(model, x_range, y_range, factor)
    elif (mode == 'integrate'):
        if (ndim == 1):
            return discretize_integrate_1D(model, x_range)
        if (ndim == 2):
            return discretize_integrate_2D(model, x_range, y_range)
    else:
        raise DiscretizationError('Invalid mode.')
