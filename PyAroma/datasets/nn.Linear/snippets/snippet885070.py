import torch
import torch.nn as nn
import torch.nn.functional as F
import math


def __init__(self, c_in, num_experts):
    super(route_func, self).__init__()
    self.avgpool = nn.AdaptiveAvgPool2d(output_size=1)
    self.fc = nn.Linear(c_in, num_experts)
    self.sigmoid = nn.Sigmoid()
