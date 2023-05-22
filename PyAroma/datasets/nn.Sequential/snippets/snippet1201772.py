import os
import sys
from functools import partial
from pretrainedmodels.models.xception import Xception
from torch.utils import model_zoo
from zoo.densenet import densenet121, densenet169, densenet161
from zoo import resnet
from zoo.dpn import dpn92
from zoo.senet import se_resnext50_32x4d, se_resnext101_32x4d, SCSEModule, senet154
import torch
from torch import nn
import torch.nn.functional as F
import numpy as np


def get_encoder(self, encoder, layer):
    if (layer == 0):
        return nn.Sequential(encoder.features.conv0, encoder.features.norm0, encoder.features.relu0)
    elif (layer == 1):
        return nn.Sequential(encoder.features.pool0, encoder.features.denseblock1)
    elif (layer == 2):
        return nn.Sequential(encoder.features.transition1, encoder.features.denseblock2)
    elif (layer == 3):
        return nn.Sequential(encoder.features.transition2, encoder.features.denseblock3)
    elif (layer == 4):
        return nn.Sequential(encoder.features.transition3, encoder.features.denseblock4, encoder.features.norm5, nn.ReLU())
