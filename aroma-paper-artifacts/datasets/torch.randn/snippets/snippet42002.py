from imresize import imresize
import math
import torch
import torch.nn as nn
import os
import sys


def generate_noise(size, num_samp=1, device='cuda', type='gaussian', scale=1):
    if (type == 'gaussian'):
        noise = torch.randn(num_samp, size[0], round((size[1] / scale)), round((size[2] / scale)), device=device)
        noise = upsampling(noise, size[1], size[2])
    if (type == 'gaussian_mixture'):
        noise1 = (torch.randn(num_samp, size[0], size[1], size[2], device=device) + 5)
        noise2 = torch.randn(num_samp, size[0], size[1], size[2], device=device)
        noise = (noise1 + noise2)
    if (type == 'uniform'):
        noise = torch.randn(num_samp, size[0], size[1], size[2], device=device)
    return noise
