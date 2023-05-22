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


def prune_layer(layer, index, dim=None):
    ' Prune a Conv1D or nn.Linear layer (a model parameters) to keep only entries in index.\n        Return the pruned layer as a new layer with requires_grad=True.\n        Used to remove heads.\n    '
    if isinstance(layer, nn.Linear):
        return prune_linear_layer(layer, index, dim=(0 if (dim is None) else dim))
    elif isinstance(layer, Conv1D):
        return prune_conv1d_layer(layer, index, dim=(1 if (dim is None) else dim))
    else:
        raise ValueError("Can't prune layer of class {}".format(layer.__class__))
