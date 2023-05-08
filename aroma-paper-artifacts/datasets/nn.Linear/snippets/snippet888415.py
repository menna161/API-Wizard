from __future__ import division
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import init
import numpy as np


def __init__(self, cardinality, depth, num_classes, widen_factor=4, dropRate=0):
    ' Constructor\n        Args:\n            cardinality: number of convolution groups.\n            depth: number of layers.\n            num_classes: number of classes\n            widen_factor: factor to adjust the channel dimensionality\n        '
    super(CifarResNeXt, self).__init__()
    self.cardinality = cardinality
    self.depth = depth
    self.block_depth = ((self.depth - 2) // 9)
    self.widen_factor = widen_factor
    self.num_classes = num_classes
    self.output_size = 64
    self.stages = [64, (64 * self.widen_factor), (128 * self.widen_factor), (256 * self.widen_factor)]
    self.conv_1_3x3 = nn.Conv2d(3, 64, 3, 1, 1, bias=False)
    self.bn_1 = nn.BatchNorm2d(64)
    self.stage_1 = self.block('stage_1', self.stages[0], self.stages[1], 1)
    self.stage_2 = self.block('stage_2', self.stages[1], self.stages[2], 2)
    self.stage_3 = self.block('stage_3', self.stages[2], self.stages[3], 2)
    self.classifier = nn.Linear(1024, num_classes)
    init.kaiming_normal(self.classifier.weight)
    for key in self.state_dict():
        if (key.split('.')[(- 1)] == 'weight'):
            if ('conv' in key):
                init.kaiming_normal(self.state_dict()[key], mode='fan_out')
            if ('bn' in key):
                self.state_dict()[key][...] = 1
        elif (key.split('.')[(- 1)] == 'bias'):
            self.state_dict()[key][...] = 0
