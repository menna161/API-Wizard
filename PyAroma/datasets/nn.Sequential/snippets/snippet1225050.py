import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from functools import partial
from collections import OrderedDict
from config import config
from resnet import get_resnet50


def __init__(self, in_channel, norm_layer, bn_momentum):
    super(SimpleRB, self).__init__()
    self.path = nn.Sequential(nn.Conv3d(in_channel, in_channel, kernel_size=3, padding=1, bias=False), norm_layer(in_channel, momentum=bn_momentum), nn.ReLU(), nn.Conv3d(in_channel, in_channel, kernel_size=3, padding=1, bias=False), norm_layer(in_channel, momentum=bn_momentum))
    self.relu = nn.ReLU()
