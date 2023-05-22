import logging
import torch
import torch.nn as nn
import torch.nn.functional as F
from mmcv.cnn import VGG, xavier_init, constant_init, kaiming_init, normal_init
from mmcv.runner import load_checkpoint
from ..registry import BACKBONES


def _make_extra_layers(self, outplanes):
    layers = []
    kernel_sizes = (1, 3)
    num_layers = 0
    outplane = None
    for i in range(len(outplanes)):
        if (self.inplanes == 'S'):
            self.inplanes = outplane
            continue
        k = kernel_sizes[(num_layers % 2)]
        if (outplanes[i] == 'S'):
            outplane = outplanes[(i + 1)]
            conv = nn.Conv2d(self.inplanes, outplane, k, stride=2, padding=1)
        else:
            outplane = outplanes[i]
            conv = nn.Conv2d(self.inplanes, outplane, k, stride=1, padding=0)
        layers.append(conv)
        self.inplanes = outplanes[i]
        num_layers += 1
    if (self.input_size == 512):
        layers.append(nn.Conv2d(self.inplanes, 256, 4, padding=1))
    return nn.Sequential(*layers)
