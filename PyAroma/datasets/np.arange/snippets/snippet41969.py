import numpy as np
from scipy.ndimage import filters, measurements, interpolation
from skimage import color
from math import pi
import torch


def contributions(in_length, out_length, scale, kernel, kernel_width, antialiasing):
    fixed_kernel = ((lambda arg: (scale * kernel((scale * arg)))) if antialiasing else kernel)
    kernel_width *= ((1.0 / scale) if antialiasing else 1.0)
    out_coordinates = np.arange(1, (out_length + 1))
    match_coordinates = (((1.0 * out_coordinates) / scale) + (0.5 * (1 - (1.0 / scale))))
    left_boundary = np.floor((match_coordinates - (kernel_width / 2)))
    expanded_kernel_width = (np.ceil(kernel_width) + 2)
    field_of_view = np.squeeze(np.uint(((np.expand_dims(left_boundary, axis=1) + np.arange(expanded_kernel_width)) - 1)))
    weights = fixed_kernel((((1.0 * np.expand_dims(match_coordinates, axis=1)) - field_of_view) - 1))
    sum_weights = np.sum(weights, axis=1)
    sum_weights[(sum_weights == 0)] = 1.0
    weights = ((1.0 * weights) / np.expand_dims(sum_weights, axis=1))
    mirror = np.uint(np.concatenate((np.arange(in_length), np.arange((in_length - 1), (- 1), step=(- 1)))))
    field_of_view = mirror[np.mod(field_of_view, mirror.shape[0])]
    non_zero_out_pixels = np.nonzero(np.any(weights, axis=0))
    weights = np.squeeze(weights[(:, non_zero_out_pixels)])
    field_of_view = np.squeeze(field_of_view[(:, non_zero_out_pixels)])
    return (weights, field_of_view)
