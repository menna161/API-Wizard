import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


def __init__(self, conv, n_feats, kernel_size, bias=True, bn=False, act=nn.ReLU(True), res_scale=1):
    super(ResBlock, self).__init__()
    m = []
    for i in range(2):
        m.append(conv(n_feats, n_feats, kernel_size, bias=bias))
        if bn:
            m.append(nn.BatchNorm2d(n_feats))
        if (i == 0):
            m.append(act)
    self.body = nn.Sequential(*m)
    self.res_scale = res_scale
