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


def _make_conv_level(self, inplanes, planes, convs, stride=1, dilation=1):
    modules = []
    for i in range(convs):
        modules.extend([nn.Conv2d(inplanes, planes, kernel_size=3, stride=(stride if (i == 0) else 1), padding=dilation, bias=False, dilation=dilation), nn.BatchNorm2d(planes, momentum=BN_MOMENTUM), nn.ReLU(inplace=True)])
        inplanes = planes
    return nn.Sequential(*modules)
