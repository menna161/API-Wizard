import numpy as np
import torch
import torch.nn as nn
from torch.nn import Parameter


def build_conv_block(self, dim, padding_type, norm_layer, use_bias):
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
    conv_block += [nn.Conv2d(dim, dim, kernel_size=3, padding=p, bias=use_bias), norm_layer(dim), nn.ReLU(True)]
    p = 0
    if (padding_type == 'reflect'):
        conv_block += [nn.ReflectionPad2d(1)]
    elif (padding_type == 'replicate'):
        conv_block += [nn.ReplicationPad2d(1)]
    elif (padding_type == 'zero'):
        p = 1
    else:
        raise NotImplementedError(('padding [%s] is not implemented' % padding_type))
    conv_block += [nn.Conv2d(dim, dim, kernel_size=3, padding=p, bias=use_bias), norm_layer(dim)]
    return nn.Sequential(*conv_block)
