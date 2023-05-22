import warnings
import os
import ctypes
from functools import partial
import numpy as np
from numpy.ctypeslib import ndpointer, load_library
from .core import Kernel, Kernel1D, Kernel2D, MAX_NORMALIZATION
from astropy.utils.exceptions import AstropyUserWarning
from astropy.utils.console import human_file_size
from astropy import units as u
from astropy.nddata import support_nddata
from astropy.modeling.core import CompoundModel
from astropy.modeling.core import SPECIAL_OPERATORS
from .utils import KernelSizeError, has_even_axis, raise_even_kernel_exception


def convolve_models(model, kernel, mode='convolve_fft', **kwargs):
    "\n    Convolve two models using `~astropy.convolution.convolve_fft`.\n\n    Parameters\n    ----------\n    model : `~astropy.modeling.core.Model`\n        Functional model\n    kernel : `~astropy.modeling.core.Model`\n        Convolution kernel\n    mode : str\n        Keyword representing which function to use for convolution.\n            * 'convolve_fft' : use `~astropy.convolution.convolve_fft` function.\n            * 'convolve' : use `~astropy.convolution.convolve`.\n    kwargs : dict\n        Keyword arguments to me passed either to `~astropy.convolution.convolve`\n        or `~astropy.convolution.convolve_fft` depending on ``mode``.\n\n    Returns\n    -------\n    default : CompoundModel\n        Convolved model\n    "
    if (mode == 'convolve_fft'):
        SPECIAL_OPERATORS['convolve_fft'] = partial(convolve_fft, **kwargs)
    elif (mode == 'convolve'):
        SPECIAL_OPERATORS['convolve'] = partial(convolve, **kwargs)
    else:
        raise ValueError(f'Mode {mode} is not supported.')
    return CompoundModel(mode, model, kernel)
