import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, in_ch, out_ch):
    super(down, self).__init__()
    self.mpconv = nn.Sequential(nn.MaxPool2d(2), double_conv(in_ch, out_ch))
