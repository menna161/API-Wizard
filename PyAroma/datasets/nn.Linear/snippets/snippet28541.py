import os
import numpy as np
from PIL import Image
import torch
from torch import nn
from torch.nn.modules.conv import _ConvNd
from torch.nn.modules.batchnorm import _BatchNorm
import torch.nn.init as initer
import torch.nn.functional as F
import socket


def group_weight2(weight_group, module, norm_layer, lr):
    group_decay = []
    group_no_decay = []
    for m in module.modules():
        if isinstance(m, nn.Linear):
            group_decay.append(m.weight)
            if (m.bias is not None):
                group_decay.append(m.bias)
        elif isinstance(m, (nn.Conv2d, nn.Conv3d)):
            group_decay.append(m.weight)
            if (m.bias is not None):
                group_decay.append(m.bias)
        elif (isinstance(m, norm_layer) or isinstance(m, nn.GroupNorm)):
            if (m.weight is not None):
                group_no_decay.append(m.weight)
            if (m.bias is not None):
                group_no_decay.append(m.bias)
    assert (len(list(module.parameters())) == (len(group_decay) + len(group_no_decay)))
    weight_group.append(dict(params=group_decay, lr=lr))
    weight_group.append(dict(params=group_no_decay, weight_decay=0.0, lr=lr))
    return weight_group
