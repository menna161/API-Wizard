import os
import numpy as np
import logging
from collections import OrderedDict
import torch
import torch.nn as nn
import torch.nn.functional as F
from core.config import cfg
import nn as mynn
import torchvision.models as models


def _init_modules(self):
    self.convs = nn.Sequential(*list(vgg.features._modules.values())[:(- 1)])
    for layer in range(10):
        for p in self.convs[layer].parameters():
            p.requires_grad = False