import os
import sys
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from collections import OrderedDict
from .sadecoder import SADecoder
from sadecoder import SADecoder


def make_classifier(classifierType='OR', num_classes=80, use_inter=False, channel1=1024, channel2=2048):
    classes = ((2 * num_classes) if (classifierType == 'OR') else num_classes)
    interout = None
    if use_inter:
        interout = nn.Sequential(OrderedDict([('dropout1', nn.Dropout2d(0.2, inplace=True)), ('conv1', nn.Conv2d(channel1, (channel1 // 2), kernel_size=3, stride=1, padding=1)), ('relu', nn.ReLU(inplace=True)), ('dropout2', nn.Dropout2d(0.2, inplace=False)), ('upsample', nn.Upsample(scale_factor=8, mode='bilinear', align_corners=True))]))
    classifier = nn.Sequential(OrderedDict([('conv', nn.Conv2d(channel2, classes, kernel_size=1, stride=1, padding=0)), ('upsample', nn.Upsample(scale_factor=8, mode='bilinear', align_corners=True))]))
    return [interout, classifier]
