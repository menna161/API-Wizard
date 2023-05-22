import math
import torch.nn as nn
from torch.nn.init import kaiming_normal_
import torchvision.transforms as transforms


def make_cls(hidden_dim):
    layers = []
    for i in range(2):
        layers += [nn.Dropout(), nn.Linear(hidden_dim, hidden_dim), nn.ReLU(inplace=True)]
    return nn.Sequential(*layers)
