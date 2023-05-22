import os
import sys
from public.path import pretrained_models_path
import torch
import torch.nn as nn
import torch.nn.functional as F


def _make_fuse_layers(self):
    if (self.num_branches == 1):
        return None
    num_branches = self.num_branches
    num_inchannels = self.num_inchannels
    fuse_layers = []
    for i in range((num_branches if self.multi_scale_output else 1)):
        fuse_layer = []
        for j in range(num_branches):
            if (j > i):
                fuse_layer.append(nn.Sequential(nn.Conv2d(num_inchannels[j], num_inchannels[i], 1, 1, 0, bias=False), nn.BatchNorm2d(num_inchannels[i]), nn.Upsample(scale_factor=(2 ** (j - i)), mode='nearest')))
            elif (j == i):
                fuse_layer.append(None)
            else:
                conv3x3s = []
                for k in range((i - j)):
                    if (k == ((i - j) - 1)):
                        num_outchannels_conv3x3 = num_inchannels[i]
                        conv3x3s.append(nn.Sequential(nn.Conv2d(num_inchannels[j], num_outchannels_conv3x3, 3, 2, 1, bias=False), nn.BatchNorm2d(num_outchannels_conv3x3)))
                    else:
                        num_outchannels_conv3x3 = num_inchannels[j]
                        conv3x3s.append(nn.Sequential(nn.Conv2d(num_inchannels[j], num_outchannels_conv3x3, 3, 2, 1, bias=False), nn.BatchNorm2d(num_outchannels_conv3x3), nn.ReLU(False)))
                fuse_layer.append(nn.Sequential(*conv3x3s))
        fuse_layers.append(nn.ModuleList(fuse_layer))
    return nn.ModuleList(fuse_layers)
