import os
import sys
from public.path import pretrained_models_path
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, w, num_classes=1000):
    super(HighResolutionNet, self).__init__()
    self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=2, padding=1, bias=False)
    self.bn1 = nn.BatchNorm2d(64)
    self.conv2 = nn.Conv2d(64, 64, kernel_size=3, stride=2, padding=1, bias=False)
    self.bn2 = nn.BatchNorm2d(64)
    self.relu = nn.ReLU(inplace=True)
    block = blocks_dict['BOTTLENECK']
    num_channels = 64
    num_blocks = 4
    self.layer1 = self._make_layer(block, 64, num_channels, num_blocks)
    stage1_out_channel = (block.expansion * num_channels)
    self.stage2_num_branches = 2
    num_channels = [(w * (2 ** mul)) for mul in range(self.stage2_num_branches)]
    block = blocks_dict['BASIC']
    stage2_config = {'NUM_MODULES': 1, 'NUM_BRANCHES': self.stage2_num_branches, 'NUM_BLOCKS': [4, 4], 'NUM_CHANNELS': num_channels, 'BLOCK': 'BASIC', 'FUSE_METHOD': 'SUM'}
    num_channels = [(num_channels[i] * block.expansion) for i in range(len(num_channels))]
    self.transition1 = self._make_transition_layer([stage1_out_channel], num_channels)
    (self.stage2, pre_stage_channels) = self._make_stage(stage2_config, num_channels)
    self.stage3_num_branches = 3
    num_channels = [(w * (2 ** mul)) for mul in range(self.stage3_num_branches)]
    block = blocks_dict['BASIC']
    stage3_config = {'NUM_MODULES': 1, 'NUM_BRANCHES': self.stage3_num_branches, 'NUM_BLOCKS': [4, 4, 4], 'NUM_CHANNELS': num_channels, 'BLOCK': 'BASIC', 'FUSE_METHOD': 'SUM'}
    num_channels = [(num_channels[i] * block.expansion) for i in range(len(num_channels))]
    self.transition2 = self._make_transition_layer(pre_stage_channels, num_channels)
    (self.stage3, pre_stage_channels) = self._make_stage(stage3_config, num_channels)
    self.stage4_num_branches = 4
    num_channels = [(w * (2 ** mul)) for mul in range(self.stage4_num_branches)]
    block = blocks_dict['BASIC']
    stage4_config = {'NUM_MODULES': 1, 'NUM_BRANCHES': self.stage4_num_branches, 'NUM_BLOCKS': [4, 4, 4, 4], 'NUM_CHANNELS': num_channels, 'BLOCK': 'BASIC', 'FUSE_METHOD': 'SUM'}
    num_channels = [(num_channels[i] * block.expansion) for i in range(len(num_channels))]
    self.transition3 = self._make_transition_layer(pre_stage_channels, num_channels)
    (self.stage4, pre_stage_channels) = self._make_stage(stage4_config, num_channels, multi_scale_output=True)
    (self.incre_modules, self.downsamp_modules, self.final_layer) = self._make_head(pre_stage_channels)
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.classifier = nn.Linear(2048, num_classes)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
        elif isinstance(m, nn.BatchNorm2d):
            nn.init.constant_(m.weight, 1)
            nn.init.constant_(m.bias, 0)
