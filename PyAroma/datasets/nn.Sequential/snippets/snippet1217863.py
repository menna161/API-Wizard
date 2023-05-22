from __future__ import print_function
import torch
import torch.nn as nn
import torch.utils.data
from torch.autograd import Variable
import torch.nn.functional as F
import math
import numpy as np


def __init__(self):
    super(feature_extraction, self).__init__()
    self.inplanes = 32
    self.firstconv = nn.Sequential(convbn(3, 32, 3, 2, 1, 1), nn.ReLU(inplace=True), convbn(32, 32, 3, 1, 1, 1), nn.ReLU(inplace=True), convbn(32, 32, 3, 1, 1, 1), nn.ReLU(inplace=True))
    self.layer1 = self._make_layer(BasicBlock, 32, 3, 1, 1, 1)
    self.layer2 = self._make_layer(BasicBlock, 64, 16, 2, 1, 1)
    self.layer3 = self._make_layer(BasicBlock, 128, 3, 1, 1, 1)
    self.layer4 = self._make_layer(BasicBlock, 128, 3, 1, 1, 2)
    self.branch1 = nn.Sequential(nn.AvgPool2d((64, 64), stride=(64, 64)), convbn(128, 32, 1, 1, 0, 1), nn.ReLU(inplace=True))
    self.branch2 = nn.Sequential(nn.AvgPool2d((32, 32), stride=(32, 32)), convbn(128, 32, 1, 1, 0, 1), nn.ReLU(inplace=True))
    self.branch3 = nn.Sequential(nn.AvgPool2d((16, 16), stride=(16, 16)), convbn(128, 32, 1, 1, 0, 1), nn.ReLU(inplace=True))
    self.branch4 = nn.Sequential(nn.AvgPool2d((8, 8), stride=(8, 8)), convbn(128, 32, 1, 1, 0, 1), nn.ReLU(inplace=True))
    self.lastconv = nn.Sequential(convbn(320, 128, 3, 1, 1, 1), nn.ReLU(inplace=True), nn.Conv2d(128, 32, kernel_size=1, padding=0, stride=1, bias=False))
