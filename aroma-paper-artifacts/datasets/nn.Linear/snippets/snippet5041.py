import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as torch_models
import numpy as np
from . import models


def __init__(self, num_class=100, num_part=15, resnet=False):
    super().__init__(num_part=num_part, resnet=resnet)
    self.linear_classifier = nn.Linear(self.dim, num_class)
    self.num_class = num_class
