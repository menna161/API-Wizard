import time
import os
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, inChannels, outChannels, **kwargs):
    super(_PPM, self).__init__()
    tempChannel = int((inChannels / 4))
    self.p1 = _Conv2D(inChannels, tempChannel, 1)
    self.p2 = _Conv2D(inChannels, tempChannel, 1)
    self.p3 = _Conv2D(inChannels, tempChannel, 1)
    self.p4 = _Conv2D(inChannels, tempChannel, 1)
    self.cat = _Conv2D((inChannels * 2), outChannels, 1)
