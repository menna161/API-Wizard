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


def build_conv_block(self, dim, padding_type, use_dropout, use_bias):
    'Construct a convolutional block.\n\n        Parameters:\n            dim (int)           -- the number of channels in the conv layer.\n            padding_type (str)  -- the name of padding layer: reflect | replicate | zero\n            norm_layer          -- normalization layer\n            use_dropout (bool)  -- if use dropout layers.\n            use_bias (bool)     -- if the conv layer uses bias or not\n\n        Returns a conv block (with a conv layer, a normalization layer, and a non-linearity layer (ReLU))\n        '
    conv_block = []
    p = 0
    if (padding_type == 'reflect'):
        conv_block += [nn.ReflectionPad2d(1)]
    elif (padding_type == 'replicate'):
        conv_block += [nn.ReplicationPad2d(1)]
    elif (padding_type == 'zero'):
        p = 1
    else:
        raise NotImplementedError(('padding [%s] is not implemented' % padding_type))
    conv_block += [nn.Conv2d(dim, dim, kernel_size=3, padding=p, bias=use_bias), nn.ReLU(True)]
    if use_dropout:
        conv_block += [nn.Dropout(0.5)]
    p = 0
    if (padding_type == 'reflect'):
        conv_block += [nn.ReflectionPad2d(1)]
    elif (padding_type == 'replicate'):
        conv_block += [nn.ReplicationPad2d(1)]
    elif (padding_type == 'zero'):
        p = 1
    else:
        raise NotImplementedError(('padding [%s] is not implemented' % padding_type))
    conv_block += [nn.Conv2d(dim, dim, kernel_size=3, padding=p, bias=use_bias)]
    return nn.Sequential(*conv_block)
