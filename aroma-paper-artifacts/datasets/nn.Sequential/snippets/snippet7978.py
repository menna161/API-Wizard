import os
import sys
from public.path import pretrained_models_path
import torch
import torch.nn as nn
import torch.nn.functional as F


def _make_transition_layer(self, num_channels_pre_layer, num_channels_cur_layer):
    num_branches_cur = len(num_channels_cur_layer)
    num_branches_pre = len(num_channels_pre_layer)
    transition_layers = []
    for i in range(num_branches_cur):
        if (i < num_branches_pre):
            if (num_channels_cur_layer[i] != num_channels_pre_layer[i]):
                transition_layers.append(nn.Sequential(nn.Conv2d(num_channels_pre_layer[i], num_channels_cur_layer[i], 3, 1, 1, bias=False), nn.BatchNorm2d(num_channels_cur_layer[i]), nn.ReLU(inplace=True)))
            else:
                transition_layers.append(None)
        else:
            conv3x3s = []
            for j in range(((i + 1) - num_branches_pre)):
                inchannels = num_channels_pre_layer[(- 1)]
                outchannels = (num_channels_cur_layer[i] if (j == (i - num_branches_pre)) else inchannels)
                conv3x3s.append(nn.Sequential(nn.Conv2d(inchannels, outchannels, 3, 2, 1, bias=False), nn.BatchNorm2d(outchannels), nn.ReLU(inplace=True)))
            transition_layers.append(nn.Sequential(*conv3x3s))
    return nn.ModuleList(transition_layers)
