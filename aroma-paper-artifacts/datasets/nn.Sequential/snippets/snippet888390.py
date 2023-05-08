import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, in_channels, out_channels, stride, t=6, class_num=100):
    super().__init__()
    self.residual = nn.Sequential(nn.Conv2d(in_channels, (in_channels * t), 1), nn.BatchNorm2d((in_channels * t)), nn.ReLU6(inplace=True), nn.Conv2d((in_channels * t), (in_channels * t), 3, stride=stride, padding=1, groups=(in_channels * t)), nn.BatchNorm2d((in_channels * t)), nn.ReLU6(inplace=True), nn.Conv2d((in_channels * t), out_channels, 1), nn.BatchNorm2d(out_channels))
    self.stride = stride
    self.in_channels = in_channels
    self.out_channels = out_channels
