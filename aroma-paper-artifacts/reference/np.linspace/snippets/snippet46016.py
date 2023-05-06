import numpy as np
import torch
import torch.nn as nn
import probabilistic_pac


def gaussian_kernel(kernel_size=5, sigma=1.0):
    'Returns a Gaussian filter kernel.'
    kernel_range = ((kernel_size - 1) / 2.0)
    distance = np.linspace((- kernel_range), kernel_range, kernel_size)
    (distance_x, distance_y) = np.meshgrid(distance, distance)
    squared_distance = ((distance_x ** 2) + (distance_y ** 2))
    gauss_kernel = np.exp((((- 0.5) * squared_distance) / np.square(sigma)))
    gauss_kernel = (gauss_kernel / np.sum(gauss_kernel))
    return torch.tensor(gauss_kernel).float().unsqueeze(0).unsqueeze(0).cuda()
