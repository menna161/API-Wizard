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


def make_final_classifier(self, in_filters, num_classes):
    return nn.Sequential(nn.Conv2d(in_filters, num_classes, 1, padding=0))
