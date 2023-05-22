import os
import sys
from public.path import pretrained_models_path
import re
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.checkpoint as cp
from collections import OrderedDict
from torch import Tensor
from torch.jit.annotations import List


def __init__(self, num_classes):
    super(Densenet161Backbone, self).__init__()
    self.model = densenet161(**{'pretrained': True})
    del self.model.classifier
    self.fc1 = nn.Linear(2208, 2048)
    self.feat_bn = nn.BatchNorm1d(2048)
    self.feat_bn.bias.requires_grad_(False)
    self.fc2 = nn.Linear(2048, num_classes)
