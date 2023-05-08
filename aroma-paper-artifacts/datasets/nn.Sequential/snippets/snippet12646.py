import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


def __init__(self):
    super(Postnet, self).__init__()
    self.convolutions = nn.ModuleList()
    self.convolutions.append(nn.Sequential(ConvNorm(80, 512, kernel_size=5, stride=1, padding=2, dilation=1, w_init_gain='tanh'), nn.BatchNorm1d(512)))
    for i in range(1, (5 - 1)):
        self.convolutions.append(nn.Sequential(ConvNorm(512, 512, kernel_size=5, stride=1, padding=2, dilation=1, w_init_gain='tanh'), nn.BatchNorm1d(512)))
    self.convolutions.append(nn.Sequential(ConvNorm(512, 80, kernel_size=5, stride=1, padding=2, dilation=1, w_init_gain='linear'), nn.BatchNorm1d(80)))
