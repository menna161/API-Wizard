import os
import sys
from functools import partial
from pretrainedmodels.models.xception import Xception
from torch.utils import model_zoo
from zoo.densenet import densenet121, densenet169, densenet161
from zoo import resnet
from zoo.dpn import dpn92
from zoo.senet import se_resnext50_32x4d, se_resnext101_32x4d, SCSEModule, senet154
import torch
from torch import nn
import torch.nn.functional as F
import numpy as np


def __init__(self, in_channels, out_channels):
    super().__init__()
    self.seq = nn.Sequential(nn.Conv2d(in_channels, out_channels, 3, padding=1), nn.ReLU(inplace=True))
