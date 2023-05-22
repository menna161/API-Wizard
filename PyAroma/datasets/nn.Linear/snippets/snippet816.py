import torch
import torch.nn as nn
import math
from layers.wavernn import WaveRNN
import utils.logger as logger
import utils.nn
import time


def __init__(self, in_channels, out_channels, global_cond_channels):
    super().__init__()
    ksz = 4
    self.out_channels = out_channels
    if (0 < global_cond_channels):
        self.w_cond = nn.Linear(global_cond_channels, (2 * out_channels), bias=False)
    self.conv_wide = nn.Conv1d(in_channels, (2 * out_channels), ksz, stride=2)
    wsize = (2.967 / math.sqrt((ksz * in_channels)))
    self.conv_wide.weight.data.uniform_((- wsize), wsize)
    self.conv_wide.bias.data.zero_()
