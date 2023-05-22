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


def _make_level(self, block, inplanes, planes, blocks, stride=1):
    downsample = None
    if ((stride != 1) or (inplanes != planes)):
        downsample = nn.Sequential(nn.MaxPool2d(stride, stride=stride), nn.Conv2d(inplanes, planes, kernel_size=1, stride=1, bias=False), nn.BatchNorm2d(planes, momentum=BN_MOMENTUM))
    layers = []
    layers.append(block(inplanes, planes, stride, downsample=downsample))
    for i in range(1, blocks):
        layers.append(block(inplanes, planes))
    return nn.Sequential(*layers)
