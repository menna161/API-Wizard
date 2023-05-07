from __future__ import print_function, division
import os
import torch
import torch.nn as nn
import numpy as np
import random
import copy


def __init__(self, fil_num, drop_rate):
    super(_CNN, self).__init__()
    self.block1 = ConvLayer(1, fil_num, 0.1, (7, 2, 0), (3, 2, 0))
    self.block2 = ConvLayer(fil_num, (2 * fil_num), 0.1, (4, 1, 0), (2, 2, 0))
    self.block3 = ConvLayer((2 * fil_num), (4 * fil_num), 0.1, (3, 1, 0), (2, 2, 0))
    self.block4 = ConvLayer((4 * fil_num), (8 * fil_num), 0.1, (3, 1, 0), (2, 1, 0))
    self.dense1 = nn.Sequential(nn.Dropout(drop_rate), nn.Linear(((((8 * fil_num) * 6) * 8) * 6), 30))
    self.dense2 = nn.Sequential(nn.LeakyReLU(), nn.Dropout(drop_rate), nn.Linear(30, 2))
