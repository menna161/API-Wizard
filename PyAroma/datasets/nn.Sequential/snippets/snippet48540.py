from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
from os.path import join
import torch
from torch import nn
import torch.utils.model_zoo as model_zoo
import numpy as np


def __init__(self, levels, block, in_channels, out_channels, stride=1, level_root=False, root_dim=0, root_kernel_size=1, dilation=1, root_residual=False):
    super(Tree, self).__init__()
    if (root_dim == 0):
        root_dim = (2 * out_channels)
    if level_root:
        root_dim += in_channels
    if (levels == 1):
        self.tree1 = block(in_channels, out_channels, stride, dilation=dilation)
        self.tree2 = block(out_channels, out_channels, 1, dilation=dilation)
    else:
        self.tree1 = Tree((levels - 1), block, in_channels, out_channels, stride, root_dim=0, root_kernel_size=root_kernel_size, dilation=dilation, root_residual=root_residual)
        self.tree2 = Tree((levels - 1), block, out_channels, out_channels, root_dim=(root_dim + out_channels), root_kernel_size=root_kernel_size, dilation=dilation, root_residual=root_residual)
    if (levels == 1):
        self.root = Root(root_dim, out_channels, root_kernel_size, root_residual)
    self.level_root = level_root
    self.root_dim = root_dim
    self.downsample = None
    self.project = None
    self.levels = levels
    if (stride > 1):
        self.downsample = nn.MaxPool2d(stride, stride=stride)
    if (in_channels != out_channels):
        self.project = nn.Sequential(nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, bias=False), BatchNorm(out_channels))