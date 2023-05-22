import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as torch_models
import numpy as np
from . import models


def __init__(self, num_class=100, resnet=False):
    super().__init__()
    if resnet:
        num_channel = 32
        self.feature_extractor = models.BackBone_ResNet(num_channel)
    else:
        num_channel = 64
        self.feature_extractor = models.BackBone(num_channel)
    self.linear_classifier = nn.Linear(num_channel, num_class)
    self.num_channel = num_channel
    self.num_class = num_class
    self.dim = num_channel
