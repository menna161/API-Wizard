import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as torch_models
import numpy as np
from . import models


def __init__(self, num_part=15, way=None, shots=None, resnet=False):
    super().__init__(way=way, shots=shots, resnet=resnet)
    num_channel = self.num_channel
    self.dim = (num_channel * num_part)
    self.num_part = num_part
    self.part_vector = nn.Parameter(torch.randn(1, num_channel, num_part, 1, 1))
