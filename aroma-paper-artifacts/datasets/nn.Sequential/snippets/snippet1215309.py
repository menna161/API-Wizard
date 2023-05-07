from __future__ import print_function, division
import os
import torch
import torch.nn as nn
import numpy as np
import random
import copy


def __init__(self, num, p):
    super(_FCN, self).__init__()
    self.features = nn.Sequential(nn.Conv3d(1, num, 4, 1, 0, bias=False), nn.MaxPool3d(2, 1, 0), nn.BatchNorm3d(num), nn.LeakyReLU(), nn.Dropout(0.1), nn.Conv3d(num, (2 * num), 4, 1, 0, bias=False), nn.MaxPool3d(2, 2, 0), nn.BatchNorm3d((2 * num)), nn.LeakyReLU(), nn.Dropout(0.1), nn.Conv3d((2 * num), (4 * num), 3, 1, 0, bias=False), nn.MaxPool3d(2, 2, 0), nn.BatchNorm3d((4 * num)), nn.LeakyReLU(), nn.Dropout(0.1), nn.Conv3d((4 * num), (8 * num), 3, 1, 0, bias=False), nn.MaxPool3d(2, 1, 0), nn.BatchNorm3d((8 * num)), nn.LeakyReLU())
    self.classifier = nn.Sequential(nn.Dropout(p), nn.Linear(((((8 * num) * 6) * 6) * 6), 30), nn.LeakyReLU(), nn.Dropout(p), nn.Linear(30, 2))
    self.feature_length = ((((8 * num) * 6) * 6) * 6)
    self.num = num
