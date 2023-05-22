import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from dropblock import DropBlock2D


def __init__(self, in_ch, out_ch, dilation, group_conv, circular_padding):
    super(down, self).__init__()
    if circular_padding:
        self.mpconv = nn.Sequential(nn.MaxPool2d(2), double_conv_circular(in_ch, out_ch, group_conv=group_conv, dilation=dilation))
    else:
        self.mpconv = nn.Sequential(nn.MaxPool2d(2), double_conv(in_ch, out_ch, group_conv=group_conv, dilation=dilation))
