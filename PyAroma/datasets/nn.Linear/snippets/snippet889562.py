import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from collections import OrderedDict
from torch.nn import init
import math
import numpy as np


def __init__(self, input_size=224, num_classes=1000):
    super(MobileNetV2, self).__init__()
    (overall_channel, mid_channel) = adapt_channel(overall_channel_ids, mid_channel_ids)
    self.feature = nn.ModuleList()
    for i in range(19):
        if (i == 0):
            self.feature.append(conv2d_3x3(3, overall_channel[i], 2))
        elif (i == 1):
            self.feature.append(bottleneck(overall_channel[(i - 1)], overall_channel[i], mid_channel[(i - 1)], 1))
        elif (i == 18):
            self.feature.append(conv2d_1x1(overall_channel[(i - 1)], 1280, 1))
        elif ((stage_out_channel[(i - 1)] != stage_out_channel[i]) and (stage_out_channel[i] != 132) and (stage_out_channel[i] != 448)):
            self.feature.append(bottleneck(overall_channel[(i - 1)], overall_channel[i], mid_channel[(i - 1)], 2))
        else:
            self.feature.append(bottleneck(overall_channel[(i - 1)], overall_channel[i], mid_channel[(i - 1)], 1))
    self.pool1 = nn.AvgPool2d(7)
    self.fc = nn.Linear(1280, 1000)
