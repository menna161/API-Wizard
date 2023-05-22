import os
import torch.nn as nn
import torch.optim as optim
from base_networks import *
from torchvision.transforms import *


def __init__(self, netVGG, feature_layer=[9, 18, 27, 36]):
    super(FeatureExtractor, self).__init__()
    self.features = nn.Sequential(*list(netVGG.features.children()))
    self.feature_layer = feature_layer
