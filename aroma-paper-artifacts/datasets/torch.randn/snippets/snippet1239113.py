import torch, numpy, itertools
import torch.nn as nn
from collections import OrderedDict


def __init__(self, size, fan_in, gain=numpy.sqrt(2)):
    super(WScaleLayer, self).__init__()
    self.scale = (gain / numpy.sqrt(fan_in))
    self.b = nn.Parameter(torch.randn(size))
    self.size = size
