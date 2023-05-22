import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


def forward(self, x):
    out = self.batch_norm(x)
    out = self.relu(out)
    if (self.dropout_rate > 0):
        out = self.dropout(out)
    self.check_if_drop()
    weight = (self.conv.weight * self.mask)
    out_conv = F.conv2d(input=out, weight=weight, bias=None, stride=self.conv.stride, padding=self.conv.padding, dilation=self.conv.dilation, groups=1)
    return out_conv
