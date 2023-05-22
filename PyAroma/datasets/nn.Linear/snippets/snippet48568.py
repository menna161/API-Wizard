from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import torch
import torch.nn as nn
from .py_utils import TopPool, BottomPool, LeftPool, RightPool


def __init__(self, inp_dim, out_dim, with_bn=True):
    super(fully_connected, self).__init__()
    self.with_bn = with_bn
    self.linear = nn.Linear(inp_dim, out_dim)
    if self.with_bn:
        self.bn = nn.BatchNorm1d(out_dim)
    self.relu = nn.ReLU(inplace=True)
