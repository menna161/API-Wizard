import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.model_zoo as model_zoo
from networks.deeplab.sync_batchnorm.batchnorm import SynchronizedBatchNorm2d
import torch


def __init__(self, inplanes, planes, reps, stride=1, dilation=1, BatchNorm=None, start_with_relu=True, grow_first=True, is_last=False):
    super(Block, self).__init__()
    if ((planes != inplanes) or (stride != 1)):
        self.skip = nn.Conv2d(inplanes, planes, 1, stride=stride, bias=False)
        self.skipbn = BatchNorm(planes)
    else:
        self.skip = None
    self.relu = nn.ReLU(inplace=True)
    rep = []
    filters = inplanes
    if grow_first:
        rep.append(self.relu)
        rep.append(SeparableConv2d(inplanes, planes, 3, 1, dilation, BatchNorm=BatchNorm))
        rep.append(BatchNorm(planes))
        filters = planes
    for i in range((reps - 1)):
        rep.append(self.relu)
        rep.append(SeparableConv2d(filters, filters, 3, 1, dilation, BatchNorm=BatchNorm))
        rep.append(BatchNorm(filters))
    if (not grow_first):
        rep.append(self.relu)
        rep.append(SeparableConv2d(inplanes, planes, 3, 1, dilation, BatchNorm=BatchNorm))
        rep.append(BatchNorm(planes))
    if (stride != 1):
        rep.append(self.relu)
        rep.append(SeparableConv2d(planes, planes, 3, 2, BatchNorm=BatchNorm))
        rep.append(BatchNorm(planes))
    if ((stride == 1) and is_last):
        rep.append(self.relu)
        rep.append(SeparableConv2d(planes, planes, 3, 1, BatchNorm=BatchNorm))
        rep.append(BatchNorm(planes))
    if (not start_with_relu):
        rep = rep[1:]
    self.rep = nn.Sequential(*rep)
