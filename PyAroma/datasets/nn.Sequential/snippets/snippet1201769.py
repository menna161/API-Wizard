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
        return nn.Sequential(encoder.blocks['conv1_1'].conv, encoder.blocks['conv1_1'].bn, encoder.blocks['conv1_1'].act)
    elif (layer == 1):
        return nn.Sequential(encoder.blocks['conv1_1'].pool, *[b for (k, b) in encoder.blocks.items() if k.startswith('conv2_')])
    elif (layer == 2):
        return nn.Sequential(*[b for (k, b) in encoder.blocks.items() if k.startswith('conv3_')])
    elif (layer == 3):
        return nn.Sequential(*[b for (k, b) in encoder.blocks.items() if k.startswith('conv4_')])
    elif (layer == 4):
        return nn.Sequential(*[b for (k, b) in encoder.blocks.items() if k.startswith('conv5_')])
