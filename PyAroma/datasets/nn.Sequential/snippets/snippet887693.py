import os
import torch.nn as nn
import torch.optim as optim
from base_networks import *
from torchvision.transforms import *


def __init__(self, resnet):
    super(FeatureExtractorResnet, self).__init__()
    self.features = nn.Sequential(*list(resnet.children())[:(- 1)])
