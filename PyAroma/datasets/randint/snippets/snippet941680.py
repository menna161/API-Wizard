import torch
import torch.nn as nn
from torch.nn import init
import functools
from torch.optim import lr_scheduler
from .vgg import Vgg19
import math
import cv2
import numpy as np
import scipy.stats as st
import code


def __call__(self, t: torch.Tensor, r: torch.Tensor, k_sz):
    device = self.device
    t = t.pow(2.2)
    r = r.pow(2.2)
    sigma = k_sz[np.random.randint(0, len(k_sz))]
    att = (1.08 + (np.random.random() / 10.0))
    alpha2 = (1 - (np.random.random() / 5.0))
    sz = int(((2 * np.ceil((2 * sigma))) + 1))
    g_kernel = get_gaussian_kernel(sz, sigma)
    g_kernel = g_kernel.to(device)
    r_blur: torch.Tensor = g_kernel(r).float()
    blend: torch.Tensor = (r_blur + t)
    maski = (blend > 1).float()
    mean_i = torch.clamp((torch.sum((blend * maski), dim=(2, 3)) / (torch.sum(maski, dim=(2, 3)) + 1e-06)), min=1).unsqueeze_((- 1)).unsqueeze_((- 1))
    r_blur = (r_blur - ((mean_i - 1) * att))
    r_blur = r_blur.clamp(min=0, max=1)
    (h, w) = r_blur.shape[2:4]
    neww = np.random.randint(0, ((560 - w) - 10))
    newh = np.random.randint(0, ((560 - h) - 10))
    alpha1 = self.g_mask[(:, newh:(newh + h), neww:(neww + w))].unsqueeze_(0)
    r_blur_mask = (r_blur * alpha1)
    blend = (r_blur_mask + (t * alpha2))
    t = t.pow((1 / 2.2))
    r_blur_mask = r_blur_mask.pow((1 / 2.2))
    blend = blend.pow((1 / 2.2))
    blend = blend.clamp(min=0, max=1)
    return (t, r_blur_mask, blend.float(), alpha2)
