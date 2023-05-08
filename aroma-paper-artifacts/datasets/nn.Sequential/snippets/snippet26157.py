import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.model_zoo as model_zoo
from torch.nn import init


def __init__(self, in_filters, out_filters, reps, strides=1, start_with_relu=True, grow_first=True):
    super(Block, self).__init__()
    if ((out_filters != in_filters) or (strides != 1)):
        self.skip = nn.Conv2d(in_filters, out_filters, 1, stride=strides, bias=False)
        self.skipbn = nn.BatchNorm2d(out_filters)
    else:
        self.skip = None
    self.relu = nn.ReLU(inplace=True)
    rep = []
    filters = in_filters
    if grow_first:
        rep.append(self.relu)
        rep.append(SeparableConv2d(in_filters, out_filters, 3, stride=1, padding=1, bias=False))
        rep.append(nn.BatchNorm2d(out_filters))
        filters = out_filters
    for i in range((reps - 1)):
        rep.append(self.relu)
        rep.append(SeparableConv2d(filters, filters, 3, stride=1, padding=1, bias=False))
        rep.append(nn.BatchNorm2d(filters))
    if (not grow_first):
        rep.append(self.relu)
        rep.append(SeparableConv2d(in_filters, out_filters, 3, stride=1, padding=1, bias=False))
        rep.append(nn.BatchNorm2d(out_filters))
    if (not start_with_relu):
        rep = rep[1:]
    else:
        rep[0] = nn.ReLU(inplace=False)
    if (strides != 1):
        rep.append(nn.MaxPool2d(3, strides, 1))
    self.rep = nn.Sequential(*rep)
