import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from dropblock import DropBlock2D


def __init__(self, in_ch, out_ch, dilation, input_batch_norm, circular_padding):
    super(inconv, self).__init__()
    if input_batch_norm:
        if circular_padding:
            self.conv = nn.Sequential(nn.BatchNorm2d(in_ch), double_conv_circular(in_ch, out_ch, group_conv=False, dilation=dilation))
        else:
            self.conv = nn.Sequential(nn.BatchNorm2d(in_ch), double_conv(in_ch, out_ch, group_conv=False, dilation=dilation))
    elif circular_padding:
        self.conv = double_conv_circular(in_ch, out_ch, group_conv=False, dilation=dilation)
    else:
        self.conv = double_conv(in_ch, out_ch, group_conv=False, dilation=dilation)
