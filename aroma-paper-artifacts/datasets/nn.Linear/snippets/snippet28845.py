import warnings
from collections import namedtuple
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils import model_zoo
import scipy.stats as stats


def __init__(self, in_channels, num_classes):
    super(InceptionAux, self).__init__()
    self.conv = BasicConv2d(in_channels, 128, kernel_size=1)
    self.fc1 = nn.Linear(2048, 1024)
    self.fc2 = nn.Linear(1024, num_classes)
