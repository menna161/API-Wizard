import os, sys
import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
import random
from utility.utils import to_one_hot
from modules.mixup import mixup_process, get_lambda
from modules.cutmix import CutMix
from data_loader import per_image_standardization
from modules.patchup import PatchUp, PatchUpMode
from modules.drop_block import DropBlock


def _wide_layer(self, block, planes, num_blocks, stride):
    strides = ([stride] + ([1] * (num_blocks - 1)))
    layers = []
    for stride in strides:
        layers.append(block(self.in_planes, planes, stride))
        self.in_planes = planes
    return nn.Sequential(*layers)
