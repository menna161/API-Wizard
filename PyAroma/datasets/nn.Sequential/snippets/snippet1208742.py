import torch
import torch.nn as nn
import torch.nn.functional as F
from dataset.config import widerface_640 as cfg


def __init__(self, C_in, C_out, kernel_size, stride, padding, dilation, affine=True, bn=False):
    super(DilConv, self).__init__()
    if (not bn):
        op = nn.Sequential(nn.Conv2d(C_in, C_in, kernel_size=kernel_size, stride=stride, padding=padding, dilation=dilation, groups=C_in, bias=True), nn.Conv2d(C_in, C_out, kernel_size=1, padding=0, bias=True))
    else:
        if cfg['GN']:
            bn_layer = nn.GroupNorm(32, C_out)
        elif cfg['syncBN']:
            bn_layer = nn.SyncBatchNorm(C_out)
        else:
            bn_layer = nn.BatchNorm2d(C_out)
        op = nn.Sequential(nn.Conv2d(C_in, C_in, kernel_size=kernel_size, stride=stride, padding=padding, dilation=dilation, groups=C_in, bias=False), nn.Conv2d(C_in, C_out, kernel_size=1, padding=0, bias=False), bn_layer)
    if RELU_FIRST:
        self.op = nn.Sequential()
        self.op.add_module('0', nn.ReLU())
        for i in range(1, (len(op) + 1)):
            self.op.add_module(str(i), op[(i - 1)])
    else:
        self.op = op
        self.op.add_module(str(len(op)), nn.ReLU())
