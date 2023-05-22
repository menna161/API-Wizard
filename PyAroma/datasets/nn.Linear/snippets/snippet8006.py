import os
import sys
from public.path import pretrained_models_path
import torch
import torch.nn as nn


def __init__(self, pretrained, num_classes):
    super(ResNet50Backbone, self).__init__()
    self.model = resnet50(**{'pretrained': pretrained})
    del self.model.fc
    self.fc1 = nn.Linear(2048, 2048)
    self.feat_bn = nn.BatchNorm1d(2048)
    self.feat_bn.bias.requires_grad_(False)
    self.fc2 = nn.Linear(2048, num_classes)
