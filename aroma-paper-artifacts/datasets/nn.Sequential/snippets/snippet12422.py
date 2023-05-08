import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
import numpy as np


def _wide_layer(self, block, planes, num_blocks, dropout_rate, stride):
    strides = ([stride] + ([1] * (num_blocks - 1)))
    layers = []
    for stride in strides:
        layers.append(block(self.in_planes, planes, dropout_rate, stride))
        self.in_planes = planes
    return nn.Sequential(*layers)
