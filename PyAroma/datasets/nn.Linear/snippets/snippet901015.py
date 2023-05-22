import math
import argparse
import time
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torchmeta.datasets.helpers import omniglot, miniimagenet
from torchmeta.utils.data import BatchMetaDataLoader
import higher
import hypergrad as hg


def initialize(net):
    for m in net.modules():
        if isinstance(m, nn.Conv2d):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
            if (m.bias is not None):
                m.bias.data.zero_()
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
        elif isinstance(m, nn.Linear):
            m.weight.data.zero_()
            m.bias.data.zero_()
    return net
