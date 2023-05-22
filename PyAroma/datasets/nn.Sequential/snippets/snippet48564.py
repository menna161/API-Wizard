from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import torch
import torch.nn as nn
from .py_utils import TopPool, BottomPool, LeftPool, RightPool


def make_hg_layer(kernel, dim0, dim1, mod, layer=convolution, **kwargs):
    layers = [layer(kernel, dim0, dim1, stride=2)]
    layers += [layer(kernel, dim1, dim1) for _ in range((mod - 1))]
    return nn.Sequential(*layers)
