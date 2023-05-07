from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import os
import torch
from torch import nn
from torch.nn import CrossEntropyLoss
from torch.nn import functional as F
from .configuration_utils import PretrainedConfig
from .file_utils import cached_path, WEIGHTS_NAME, TF_WEIGHTS_NAME
from torch.nn import Identity


def prune_linear_layer(layer, index, dim=0):
    ' Prune a linear layer (a model parameters) to keep only entries in index.\n        Return the pruned layer as a new layer with requires_grad=True.\n        Used to remove heads.\n    '
    index = index.to(layer.weight.device)
    W = layer.weight.index_select(dim, index).clone().detach()
    if (layer.bias is not None):
        if (dim == 1):
            b = layer.bias.clone().detach()
        else:
            b = layer.bias[index].clone().detach()
    new_size = list(layer.weight.size())
    new_size[dim] = len(index)
    new_layer = nn.Linear(new_size[1], new_size[0], bias=(layer.bias is not None)).to(layer.weight.device)
    new_layer.weight.requires_grad = False
    new_layer.weight.copy_(W.contiguous())
    new_layer.weight.requires_grad = True
    if (layer.bias is not None):
        new_layer.bias.requires_grad = False
        new_layer.bias.copy_(b.contiguous())
        new_layer.bias.requires_grad = True
    return new_layer
