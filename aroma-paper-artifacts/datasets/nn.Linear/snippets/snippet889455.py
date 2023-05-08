import torch.nn as nn
import math
import torch.utils.model_zoo as model_zoo
import mmd
import torch
import torch.nn.functional as F
import random


def __init__(self, in_channels, pool_features, num_classes):
    super(InceptionA, self).__init__()
    self.branch1x1 = BasicConv2d(in_channels, 64, kernel_size=1)
    self.branch5x5_1 = BasicConv2d(in_channels, 48, kernel_size=1)
    self.branch5x5_2 = BasicConv2d(48, 64, kernel_size=5, padding=2)
    self.branch3x3dbl_1 = BasicConv2d(in_channels, 64, kernel_size=1)
    self.branch3x3dbl_2 = BasicConv2d(64, 96, kernel_size=3, padding=1)
    self.branch3x3dbl_3 = BasicConv2d(96, 96, kernel_size=3, padding=1)
    self.branch_pool = BasicConv2d(in_channels, pool_features, kernel_size=1)
    self.avg_pool = nn.AvgPool2d(7, stride=1)
    self.source_fc = nn.Linear(288, num_classes)
