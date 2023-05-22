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


def __init__(self, in_planes, planes, stride=1):
    super(wide_basic, self).__init__()
    self.bn1 = nn.BatchNorm2d(in_planes)
    self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=3, padding=1, bias=True)
    self.bn2 = nn.BatchNorm2d(planes)
    self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=True)
    self.shortcut = nn.Sequential()
    if ((stride != 1) or (in_planes != planes)):
        self.shortcut = nn.Sequential(nn.Conv2d(in_planes, planes, kernel_size=1, stride=stride, bias=True))
