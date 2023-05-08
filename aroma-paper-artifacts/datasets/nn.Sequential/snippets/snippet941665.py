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


def __init__(self, input_nc, ndf=64, norm_layer=nn.BatchNorm2d):
    'Construct a 1x1 PatchGAN discriminator\n\n        Parameters:\n            input_nc (int)  -- the number of channels in input images\n            ndf (int)       -- the number of filters in the last conv layer\n            norm_layer      -- normalization layer\n        '
    super(PixelDiscriminator, self).__init__()
    if (type(norm_layer) == functools.partial):
        use_bias = (norm_layer.func != nn.InstanceNorm2d)
    else:
        use_bias = (norm_layer != nn.InstanceNorm2d)
    self.net = [nn.Conv2d(input_nc, ndf, kernel_size=1, stride=1, padding=0), nn.LeakyReLU(0.2, True), nn.Conv2d(ndf, (ndf * 2), kernel_size=1, stride=1, padding=0, bias=use_bias), norm_layer((ndf * 2)), nn.LeakyReLU(0.2, True), nn.Conv2d((ndf * 2), 1, kernel_size=1, stride=1, padding=0, bias=use_bias)]
    self.net = nn.Sequential(*self.net)
