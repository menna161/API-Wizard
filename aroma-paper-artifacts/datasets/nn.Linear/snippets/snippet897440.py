import functools
import torch
from torch import nn
import torch.nn.functional as F
from torch.nn.modules.conv import _ConvNd
from torch.nn.modules.utils import _pair
from torch.nn.parameter import Parameter


def __init__(self, in_channels, num_experts, dropout_rate):
    super(_routing, self).__init__()
    self.dropout = nn.Dropout(dropout_rate)
    self.fc = nn.Linear(in_channels, num_experts)
