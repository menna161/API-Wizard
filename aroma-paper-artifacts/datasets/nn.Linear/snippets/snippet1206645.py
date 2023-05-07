from __future__ import division
import torch
import torch.nn as nn
import torch.nn.functional as F
from gcn.layers import GConv


def __init__(self, channel=4):
    super(GCN, self).__init__()
    self.channel = channel
    self.model = nn.Sequential(GConv(1, 10, 5, padding=2, stride=1, M=channel, nScale=1, bias=False, expand=True), nn.BatchNorm2d((10 * channel)), nn.ReLU(inplace=True), GConv(10, 20, 5, padding=2, stride=1, M=channel, nScale=2, bias=False), nn.BatchNorm2d((20 * channel)), nn.ReLU(inplace=True), nn.MaxPool2d(2, 2), GConv(20, 40, 5, padding=0, stride=1, M=channel, nScale=3, bias=False), nn.BatchNorm2d((40 * channel)), nn.ReLU(inplace=True), nn.MaxPool2d(2, 2), GConv(40, 80, 5, padding=0, stride=1, M=channel, nScale=4, bias=False), nn.BatchNorm2d((80 * channel)), nn.ReLU(inplace=True))
    self.fc1 = nn.Linear(80, 1024)
    self.relu = nn.ReLU(inplace=True)
    self.dropout = nn.Dropout(p=0.5)
    self.fc2 = nn.Linear(1024, 10)
