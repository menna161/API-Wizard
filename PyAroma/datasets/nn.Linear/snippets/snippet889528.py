import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from collections import OrderedDict
from torch.nn import init
import math
import numpy as np


def __init__(self, input_size=224, num_classes=1000):
    super(MobileNetV1, self).__init__()
    self.feature = nn.ModuleList()
    self.feature.append(Select_conv1(3, stage_out_channel[0], 2))
    for i in range(1, len(stage_out_channel)):
        if ((stage_out_channel[(i - 1)] != stage_out_channel[i]) and (stage_out_channel[i] != 64)):
            self.feature.append(Select_one_OP(stage_out_channel[(i - 1)], stage_out_channel[i], 2))
        else:
            self.feature.append(Select_one_OP(stage_out_channel[(i - 1)], stage_out_channel[i], 1))
    self.pool1 = nn.AvgPool2d(7)
    self.fc = nn.Linear(1024, 1000)
