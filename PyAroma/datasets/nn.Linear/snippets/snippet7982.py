import os
import sys
from public.path import pretrained_models_path
import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, num_classes):
    super(Hrnetw18Backbone, self).__init__()
    self.model = HRNet_W18(**{'pretrained': True})
    del self.model.classifier
    self.fc1 = nn.Linear(2048, 2048)
    self.feat_bn = nn.BatchNorm1d(2048)
    self.feat_bn.bias.requires_grad_(False)
    self.fc2 = nn.Linear(2048, num_classes)
