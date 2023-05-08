import torch
import torch.nn as nn
import torch.utils.model_zoo as model_zoo
import torch.nn.functional as F


def __init__(self, num_classes=1000):
    super(ResNet50, self).__init__()
    self.layers = nn.ModuleList()
    self.layers.append(first_conv_block(3, 64, stride=2))
    self.layers.append(Bottleneck(64, 256, stride=1, is_downsample=True))
    for i in range(1, stage_repeat[0]):
        self.layers.append(Bottleneck(256, 256))
    self.layers.append(Bottleneck(256, 512, stride=2, is_downsample=True))
    for i in range(1, stage_repeat[1]):
        self.layers.append(Bottleneck(512, 512))
    self.layers.append(Bottleneck(512, 1024, stride=2, is_downsample=True))
    for i in range(1, stage_repeat[2]):
        self.layers.append(Bottleneck(1024, 1024))
    self.layers.append(Bottleneck(1024, 2048, stride=2, is_downsample=True))
    for i in range(1, stage_repeat[3]):
        self.layers.append(Bottleneck(2048, 2048))
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.fc = nn.Linear(2048, num_classes)
