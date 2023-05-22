import os
import sys
from public.path import pretrained_models_path
import torch
import torch.nn as nn
import torch.nn.functional as F


def _make_head(self, pre_stage_channels):
    head_block = Bottleneck
    head_channels = [32, 64, 128, 256]
    incre_modules = []
    for (i, channels) in enumerate(pre_stage_channels):
        incre_module = self._make_layer(head_block, channels, head_channels[i], 1, stride=1)
        incre_modules.append(incre_module)
    incre_modules = nn.ModuleList(incre_modules)
    downsamp_modules = []
    for i in range((len(pre_stage_channels) - 1)):
        in_channels = (head_channels[i] * head_block.expansion)
        out_channels = (head_channels[(i + 1)] * head_block.expansion)
        downsamp_module = nn.Sequential(nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=3, stride=2, padding=1), nn.BatchNorm2d(out_channels), nn.ReLU(inplace=True))
        downsamp_modules.append(downsamp_module)
    downsamp_modules = nn.ModuleList(downsamp_modules)
    final_layer = nn.Sequential(nn.Conv2d(in_channels=(head_channels[3] * head_block.expansion), out_channels=2048, kernel_size=1, stride=1, padding=0), nn.BatchNorm2d(2048), nn.ReLU(inplace=True))
    return (incre_modules, downsamp_modules, final_layer)
