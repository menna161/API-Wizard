import numpy as np
from scipy.ndimage import filters, measurements, interpolation
from skimage import color
from math import pi
import torch


def numeric_kernel(im, kernel, scale_factor, output_shape, kernel_shift_flag):
    if kernel_shift_flag:
        kernel = kernel_shift(kernel, scale_factor)
    out_im = np.zeros_like(im)
    for channel in range(np.ndim(im)):
        out_im[(:, :, channel)] = filters.correlate(im[(:, :, channel)], kernel)
    return out_im[(np.round(np.linspace(0, (im.shape[0] - (1 / scale_factor[0])), output_shape[0])).astype(int)[(:, None)], np.round(np.linspace(0, (im.shape[1] - (1 / scale_factor[1])), output_shape[1])).astype(int), :)]
