import time
import os
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, dsc1, dsc2, dsc2out, **kwargs):
    super(LearningToDownSample, self).__init__()
    self.conv = _Conv2D(3, dsc1, 3, 2)
    self.dsc1 = _DSConv(dsc1, dsc2, 2)
    self.dsc2 = _DSConv(dsc2, dsc2out, 2)
