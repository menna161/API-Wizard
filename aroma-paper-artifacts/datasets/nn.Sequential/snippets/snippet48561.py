from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import torch
import torch.nn as nn
from .py_utils import TopPool, BottomPool, LeftPool, RightPool


def make_kp_layer(cnv_dim, curr_dim, out_dim):
    return nn.Sequential(convolution(3, cnv_dim, curr_dim, with_bn=False), nn.Conv2d(curr_dim, out_dim, (1, 1)))
