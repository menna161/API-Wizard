import warnings
from collections import namedtuple
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils import model_zoo
import scipy.stats as stats


def __init__(self, num_classes=1000, aux_logits=True, transform_input=False, init_weights=True):
    super(GoogLeNet, self).__init__()
    self.aux_logits = aux_logits
    self.transform_input = transform_input
    self.conv1 = BasicConv2d(3, 64, kernel_size=7, stride=2, padding=3)
    self.maxpool1 = nn.MaxPool2d(3, stride=2, ceil_mode=True)
    self.conv2 = BasicConv2d(64, 64, kernel_size=1)
    self.conv3 = BasicConv2d(64, 192, kernel_size=3, padding=1)
    self.maxpool2 = nn.MaxPool2d(3, stride=2, ceil_mode=True)
    self.inception3a = Inception(192, 64, 96, 128, 16, 32, 32)
    self.inception3b = Inception(256, 128, 128, 192, 32, 96, 64)
    self.maxpool3 = nn.MaxPool2d(3, stride=2, ceil_mode=True)
    self.inception4a = Inception(480, 192, 96, 208, 16, 48, 64)
    self.inception4b = Inception(512, 160, 112, 224, 24, 64, 64)
    self.inception4c = Inception(512, 128, 128, 256, 24, 64, 64)
    self.inception4d = Inception(512, 112, 144, 288, 32, 64, 64)
    self.inception4e = Inception(528, 256, 160, 320, 32, 128, 128)
    self.maxpool4 = nn.MaxPool2d(2, stride=2, ceil_mode=True)
    self.inception5a = Inception(832, 256, 160, 320, 32, 128, 128)
    self.inception5b = Inception(832, 384, 192, 384, 48, 128, 128)
    if aux_logits:
        self.aux1 = InceptionAux(512, num_classes)
        self.aux2 = InceptionAux(528, num_classes)
    self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    self.dropout = nn.Dropout(0.2)
    self.fc = nn.Linear(1024, num_classes)
    if init_weights:
        self._initialize_weights()
