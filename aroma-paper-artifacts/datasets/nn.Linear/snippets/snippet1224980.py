from collections import OrderedDict
import numpy as np
import torch
import torch.nn as nn


def __init__(self, in_planes, out_planes, reduction=16):
    super(SELayer, self).__init__()
    self.avg_pool = nn.AdaptiveAvgPool2d(1)
    self.fc = nn.Sequential(nn.Linear(in_planes, (out_planes // reduction)), nn.ReLU(inplace=True), nn.Linear((out_planes // reduction), out_planes), nn.Sigmoid())
    self.out_planes = out_planes
