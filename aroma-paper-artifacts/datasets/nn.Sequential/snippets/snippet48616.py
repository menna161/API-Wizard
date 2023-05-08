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


def __init__(self, chi, cho):
    super(DeformConv, self).__init__()
    self.actf = nn.Sequential(nn.BatchNorm2d(cho, momentum=BN_MOMENTUM), nn.ReLU(inplace=True))
    self.conv = DCN(chi, cho, kernel_size=(3, 3), stride=1, padding=1, dilation=1, deformable_groups=1)
