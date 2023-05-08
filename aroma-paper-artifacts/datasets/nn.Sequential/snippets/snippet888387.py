import torch
import torch.nn as nn


def __init__(self, num_class=100):
    super().__init__()
    self.prelayer = nn.Sequential(nn.Conv2d(3, 192, kernel_size=3, padding=1), nn.BatchNorm2d(192), nn.ReLU(inplace=True))
    self.a3 = Inception(192, 64, 96, 128, 16, 32, 32)
    self.b3 = Inception(256, 128, 128, 192, 32, 96, 64)
    self.maxpool = nn.MaxPool2d(3, stride=2, padding=1)
    self.a4 = Inception(480, 192, 96, 208, 16, 48, 64)
    self.b4 = Inception(512, 160, 112, 224, 24, 64, 64)
    self.c4 = Inception(512, 128, 128, 256, 24, 64, 64)
    self.d4 = Inception(512, 112, 144, 288, 32, 64, 64)
    self.e4 = Inception(528, 256, 160, 320, 32, 128, 128)
    self.a5 = Inception(832, 256, 160, 320, 32, 128, 128)
    self.b5 = Inception(832, 384, 192, 384, 48, 128, 128)
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.dropout = nn.Dropout2d(p=0.4)
    self.linear = nn.Linear(1024, num_class)
