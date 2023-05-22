import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as torch_models
import numpy as np


def __init__(self, num_channel=64):
    super().__init__()
    self.layers = nn.Sequential(ConvBlock(3, num_channel), nn.ReLU(inplace=True), nn.MaxPool2d(2), ConvBlock(num_channel, num_channel), nn.ReLU(inplace=True), nn.MaxPool2d(2), ConvBlock(num_channel, num_channel), nn.ReLU(inplace=True), nn.MaxPool2d(2), ConvBlock(num_channel, num_channel))
