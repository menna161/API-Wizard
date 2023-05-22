import os
import sys
from public.path import pretrained_models_path
import torch
import torch.nn as nn
import torch.nn.functional as F


def _make_one_branch(self, branch_index, block, num_blocks, num_channels, stride=1):
    downsample = None
    if ((stride != 1) or (self.num_inchannels[branch_index] != (num_channels[branch_index] * block.expansion))):
        downsample = nn.Sequential(nn.Conv2d(self.num_inchannels[branch_index], (num_channels[branch_index] * block.expansion), kernel_size=1, stride=stride, bias=False), nn.BatchNorm2d((num_channels[branch_index] * block.expansion)))
    layers = []
    layers.append(block(self.num_inchannels[branch_index], num_channels[branch_index], stride, downsample))
    self.num_inchannels[branch_index] = (num_channels[branch_index] * block.expansion)
    for i in range(1, num_blocks[branch_index]):
        layers.append(block(self.num_inchannels[branch_index], num_channels[branch_index]))
    return nn.Sequential(*layers)
