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
        return nn.Sequential(encoder.conv1, encoder.bn1, encoder.relu)
    elif (layer == 1):
        return nn.Sequential(encoder.maxpool, encoder.layer1)
    elif (layer == 2):
        return encoder.layer2
    elif (layer == 3):
        return encoder.layer3
    elif (layer == 4):
        return encoder.layer4
