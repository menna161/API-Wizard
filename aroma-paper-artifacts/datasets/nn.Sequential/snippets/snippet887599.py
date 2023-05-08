import torch.nn as nn
import math
import torch
import numpy as np
import torch.nn.functional as F


def __init__(self, block, layers):
    super(ResNet_locate, self).__init__()
    self.resnet = ResNet(block, layers)
    self.in_planes = 512
    self.out_planes = [512, 256, 256, 128]
    self.ppms_pre = nn.Conv2d(2048, self.in_planes, 1, 1, bias=False)
    (ppms, infos) = ([], [])
    for ii in [1, 3, 5]:
        ppms.append(nn.Sequential(nn.AdaptiveAvgPool2d(ii), nn.Conv2d(self.in_planes, self.in_planes, 1, 1, bias=False), nn.ReLU(inplace=True)))
    self.ppms = nn.ModuleList(ppms)
    self.ppm_cat = nn.Sequential(nn.Conv2d((self.in_planes * 4), self.in_planes, 3, 1, 1, bias=False), nn.ReLU(inplace=True))
    for ii in self.out_planes:
        infos.append(nn.Sequential(nn.Conv2d(self.in_planes, ii, 3, 1, 1, bias=False), nn.ReLU(inplace=True)))
    self.infos = nn.ModuleList(infos)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, 0.01)
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
