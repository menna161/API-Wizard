import math
import numbers
import numpy as np
import torch
import torch.nn.functional as F
import torch.nn as nn


def make_kernels(snow_length_bound=13, blur=True):
    kernels = []
    flip = (np.random.uniform() < 0.5)
    for i in range(7):
        k_size = snow_length_bound
        mid = (k_size // 2)
        k_npy = np.zeros((k_size, k_size))
        (rr, cc, val) = weighted_line(mid, mid, np.random.randint((mid + 2), k_size), np.random.randint((mid + 2), k_size), np.random.choice([1, 3, 5], p=[0.6, 0.3, 0.1]), mid, k_size)
        k_npy[(rr, cc)] = val
        k_npy[:(mid + 1), :(mid + 1)] = k_npy[::(- 1), ::(- 1)][:(mid + 1), :(mid + 1)]
        if flip:
            k_npy = k_npy[:, ::(- 1)]
        kernel = torch.FloatTensor(k_npy.copy()).view(1, 1, k_size, k_size).cuda()
        if blur:
            blurriness = np.random.uniform(0.41, 0.6)
            gaussian_blur = GaussianSmoothing(int(np.ceil((5 * blurriness))), blurriness)
            kernel = gaussian_blur(kernel, padding=1)
        kernels.append(kernel)
    return kernels
