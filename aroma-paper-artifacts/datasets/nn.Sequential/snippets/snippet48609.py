from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import math
import logging
import numpy as np
from os.path import join
import torch
from torch import nn
import torch.nn.functional as F
import torch.utils.model_zoo as model_zoo
from .DCNv2.dcn_v2 import DCN


def __init__(self, levels, channels, num_classes=1000, block=BasicBlock, residual_root=False, linear_root=False):
    super(DLA, self).__init__()
    self.channels = channels
    self.num_classes = num_classes
    self.base_layer = nn.Sequential(nn.Conv2d(3, channels[0], kernel_size=7, stride=1, padding=3, bias=False), nn.BatchNorm2d(channels[0], momentum=BN_MOMENTUM), nn.ReLU(inplace=True))
    self.level0 = self._make_conv_level(channels[0], channels[0], levels[0])
    self.level1 = self._make_conv_level(channels[0], channels[1], levels[1], stride=2)
    self.level2 = Tree(levels[2], block, channels[1], channels[2], 2, level_root=False, root_residual=residual_root)
    self.level3 = Tree(levels[3], block, channels[2], channels[3], 2, level_root=True, root_residual=residual_root)
    self.level4 = Tree(levels[4], block, channels[3], channels[4], 2, level_root=True, root_residual=residual_root)
    self.level5 = Tree(levels[5], block, channels[4], channels[5], 2, level_root=True, root_residual=residual_root)
