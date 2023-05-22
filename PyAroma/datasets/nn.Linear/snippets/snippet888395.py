import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, params):
    '\n        We define an convolutional network that predicts the sign from an image. The components\n        required are:\n        Args:\n            params: (Params) contains num_channels\n        '
    super(Net, self).__init__()
    self.num_channels = params.num_channels
    self.conv1 = nn.Conv2d(3, self.num_channels, 3, stride=1, padding=1)
    self.bn1 = nn.BatchNorm2d(self.num_channels)
    self.conv2 = nn.Conv2d(self.num_channels, (self.num_channels * 2), 3, stride=1, padding=1)
    self.bn2 = nn.BatchNorm2d((self.num_channels * 2))
    self.conv3 = nn.Conv2d((self.num_channels * 2), (self.num_channels * 4), 3, stride=1, padding=1)
    self.bn3 = nn.BatchNorm2d((self.num_channels * 4))
    self.fc1 = nn.Linear((((4 * 4) * self.num_channels) * 4), (self.num_channels * 4))
    self.fcbn1 = nn.BatchNorm1d((self.num_channels * 4))
    self.fc2 = nn.Linear((self.num_channels * 4), params.num_class)
    self.dropout_rate = params.dropout_rate
