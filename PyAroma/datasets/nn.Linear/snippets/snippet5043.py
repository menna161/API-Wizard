import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as torch_models
import numpy as np
from . import models


def __init__(self, num_class=100, num_part=15, resnet=False):
    super().__init__()
    if resnet:
        num_channel = 32
        self.feature_extractor = models.BackBone_ResNet(num_channel)
    else:
        num_channel = 64
        self.feature_extractor = models.BackBone(num_channel)
    self.num_channel = num_channel
    self.num_part = num_part
    self.num_class = num_class
    self.dim = (num_channel * num_part)
    self.linear_classifier = nn.Linear(self.dim, num_class)
