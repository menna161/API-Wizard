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


def __init__(self, outer_nc, inner_nc, input_nc=None, submodule=None, outermost=False, innermost=False, norm_layer=nn.BatchNorm2d, use_dropout=False):
    'Construct a Unet submodule with skip connections.\n\n        Parameters:\n            outer_nc (int) -- the number of filters in the outer conv layer\n            inner_nc (int) -- the number of filters in the inner conv layer\n            input_nc (int) -- the number of channels in input images/features\n            submodule (UnetSkipConnectionBlock) -- previously defined submodules\n            outermost (bool)    -- if this module is the outermost module\n            innermost (bool)    -- if this module is the innermost module\n            norm_layer          -- normalization layer\n            user_dropout (bool) -- if use dropout layers.\n        '
    super(UnetSkipConnectionBlock, self).__init__()
    self.outermost = outermost
    if (type(norm_layer) == functools.partial):
        use_bias = (norm_layer.func == nn.InstanceNorm2d)
    else:
        use_bias = (norm_layer == nn.InstanceNorm2d)
    if (input_nc is None):
        input_nc = outer_nc
    downconv = nn.Conv2d(input_nc, inner_nc, kernel_size=4, stride=2, padding=1, bias=use_bias)
    downrelu = nn.LeakyReLU(0.2, True)
    downnorm = norm_layer(inner_nc)
    uprelu = nn.ReLU(True)
    upnorm = norm_layer(outer_nc)
    if outermost:
        upconv = nn.ConvTranspose2d((inner_nc * 2), outer_nc, kernel_size=4, stride=2, padding=1)
        down = [downconv]
        up = [uprelu, upconv, nn.Tanh()]
        model = ((down + [submodule]) + up)
    elif innermost:
        upconv = nn.ConvTranspose2d(inner_nc, outer_nc, kernel_size=4, stride=2, padding=1, bias=use_bias)
        down = [downrelu, downconv]
        up = [uprelu, upconv, upnorm]
        model = (down + up)
    else:
        upconv = nn.ConvTranspose2d((inner_nc * 2), outer_nc, kernel_size=4, stride=2, padding=1, bias=use_bias)
        down = [downrelu, downconv, downnorm]
        up = [uprelu, upconv, upnorm]
        if use_dropout:
            model = (((down + [submodule]) + up) + [nn.Dropout(0.5)])
        else:
            model = ((down + [submodule]) + up)
    self.model = nn.Sequential(*model)
