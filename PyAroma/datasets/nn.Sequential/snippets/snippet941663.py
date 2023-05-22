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


def __init__(self, input_nc, ndf=64, n_layers=3, norm_layer=nn.BatchNorm2d):
    'Construct a PatchGAN discriminator\n\n        Parameters:\n            input_nc (int)  -- the number of channels in input images\n            ndf (int)       -- the number of filters in the last conv layer\n            n_layers (int)  -- the number of conv layers in the discriminator\n            norm_layer      -- normalization layer\n        '
    super(NLayerDiscriminator, self).__init__()
    if (type(norm_layer) == functools.partial):
        use_bias = (norm_layer.func != nn.BatchNorm2d)
    else:
        use_bias = (norm_layer != nn.BatchNorm2d)
    kw = 4
    padw = 1
    sequence = [nn.Conv2d(input_nc, ndf, kernel_size=kw, stride=2, padding=padw), nn.LeakyReLU(0.2, True)]
    nf_mult = 1
    nf_mult_prev = 1
    for n in range(1, n_layers):
        nf_mult_prev = nf_mult
        nf_mult = min((2 ** n), 8)
        sequence += [nn.Conv2d((ndf * nf_mult_prev), (ndf * nf_mult), kernel_size=kw, stride=2, padding=padw, bias=use_bias), norm_layer((ndf * nf_mult)), nn.LeakyReLU(0.2, True)]
    nf_mult_prev = nf_mult
    nf_mult = min((2 ** n_layers), 8)
    sequence += [nn.Conv2d((ndf * nf_mult_prev), (ndf * nf_mult), kernel_size=kw, stride=1, padding=padw, bias=use_bias), norm_layer((ndf * nf_mult)), nn.LeakyReLU(0.2, True)]
    sequence += [nn.Conv2d((ndf * nf_mult), 1, kernel_size=kw, stride=1, padding=padw)]
    self.model = nn.Sequential(*sequence)
