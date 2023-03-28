import random
import numpy as np
import torch
import torch.nn as nn
import scipy.sparse as sparse
from advex_uar.attacks.attacks import AttackWrapper
from advex_uar.attacks.gabor import get_gabor_with_sides, valid_position, gabor_rand_distributed


def _get_gabor_kernel(self, batch_size):
    k_size = 23
    kernels = []
    for b in range(batch_size):
        sides = (np.random.randint(10) + 1)
        sigma = ((0.3 * torch.rand(1)) + 0.1)
        Lambda = ((((k_size / 4.0) - 3) * torch.rand(1)) + 3)
        theta = (np.pi * torch.rand(1))
        kernels.append(get_gabor_with_sides(k_size, sigma, Lambda, theta, sides).cuda())
    gabor_kernel = torch.cat(kernels, 0).view((- 1), 1, k_size, k_size)
    return gabor_kernel
