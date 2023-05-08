import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as torch_models
import numpy as np


def __init__(self, num_part, resnet=False):
    super().__init__()
    if resnet:
        num_channel = 32
        resnet18 = torch_models.resnet18()
        conv1 = resnet18.conv1
        bn1 = resnet18.bn1
        relu = resnet18.relu
        maxpool = resnet18.maxpool
        layer1 = resnet18.layer1
        layer2 = resnet18.layer2
        layer3 = resnet18.layer3
        layer4 = resnet18.layer4
        layer4[0].conv1 = nn.Conv2d(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        layer4[0].downsample[0] = nn.Conv2d(256, 512, kernel_size=(1, 1), stride=(1, 1), bias=False)
        layer5 = nn.Sequential(nn.Conv2d(512, num_channel, kernel_size=1, stride=1, padding=0), nn.BatchNorm2d(num_channel))
        self.shared_layers = nn.Sequential(conv1, bn1, relu, maxpool, layer1, layer2, layer3)
        self.class_branch = nn.Sequential(layer4, layer5)
        self.part_branch = nn.Sequential(nn.Conv2d(256, 64, kernel_size=3, stride=1, padding=1), nn.BatchNorm2d(64), nn.ReLU(inplace=True), nn.Conv2d(64, num_part, kernel_size=3, stride=1, padding=1))
        del resnet18
    else:
        num_channel = 64
        self.shared_layers = nn.Sequential(ConvBlock(3, num_channel), nn.ReLU(inplace=True), nn.MaxPool2d(2), ConvBlock(num_channel, num_channel), nn.ReLU(inplace=True), nn.MaxPool2d(2))
        self.part_branch = nn.Sequential(nn.Conv2d(num_channel, 30, kernel_size=3, stride=2, padding=0), nn.BatchNorm2d(30), nn.ReLU(inplace=True), nn.Conv2d(30, num_part, kernel_size=3, stride=1, padding=1))
        self.class_branch = nn.Sequential(ConvBlock(num_channel, num_channel), nn.ReLU(inplace=True), nn.MaxPool2d(2), ConvBlock(num_channel, num_channel))
    self.num_channel = num_channel
    self.num_part = num_part
    self.dim = (num_channel * num_part)
