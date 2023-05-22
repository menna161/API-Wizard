import torch
import torch.nn as nn
from torch.nn import init
import functools
from torch.optim import lr_scheduler
from deeplab import Deeplab
from collections import OrderedDict
import torch.nn.functional as F
from fcn8s_LSD import FCN8s_LSD


def build_conv_block(self, dim, padding_type, norm_layer, use_dropout, use_bias):
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
    conv_block += [nn.Conv2d(dim, dim, kernel_size=3, padding=p, bias=use_bias), norm_layer(dim)]
    return nn.Sequential(*conv_block)
