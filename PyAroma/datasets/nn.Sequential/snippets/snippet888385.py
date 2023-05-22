import torch
import torch.nn as nn


def __init__(self, input_channels, n1x1, n3x3_reduce, n3x3, n5x5_reduce, n5x5, pool_proj):
    super().__init__()
    self.b1 = nn.Sequential(nn.Conv2d(input_channels, n1x1, kernel_size=1), nn.BatchNorm2d(n1x1), nn.ReLU(inplace=True))
    self.b2 = nn.Sequential(nn.Conv2d(input_channels, n3x3_reduce, kernel_size=1), nn.BatchNorm2d(n3x3_reduce), nn.ReLU(inplace=True), nn.Conv2d(n3x3_reduce, n3x3, kernel_size=3, padding=1), nn.BatchNorm2d(n3x3), nn.ReLU(inplace=True))
    self.b3 = nn.Sequential(nn.Conv2d(input_channels, n5x5_reduce, kernel_size=1), nn.BatchNorm2d(n5x5_reduce), nn.ReLU(inplace=True), nn.Conv2d(n5x5_reduce, n5x5, kernel_size=3, padding=1), nn.BatchNorm2d(n5x5, n5x5), nn.ReLU(inplace=True), nn.Conv2d(n5x5, n5x5, kernel_size=3, padding=1), nn.BatchNorm2d(n5x5), nn.ReLU(inplace=True))
    self.b4 = nn.Sequential(nn.MaxPool2d(3, stride=1, padding=1), nn.Conv2d(input_channels, pool_proj, kernel_size=1), nn.BatchNorm2d(pool_proj), nn.ReLU(inplace=True))
