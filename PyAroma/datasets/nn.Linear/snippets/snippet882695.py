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


def __init__(self, depth, widen_factor, num_classes, per_img_std=False, stride=1, drop_block=7, keep_prob=0.9, gamma=0.9, patchup_block=7):
    super(Wide_ResNet, self).__init__()
    self.num_classes = num_classes
    self.per_img_std = per_img_std
    self.in_planes = 16
    assert (((depth - 4) % 6) == 0), 'Wide-resnet_v2 depth should be 6n+4'
    n = int(((depth - 4) / 6))
    k = widen_factor
    print(('| Wide-Resnet %dx%d' % (depth, k)))
    nStages = [16, (16 * k), (32 * k), (64 * k)]
    self.keep_prob = keep_prob
    self.gamma = gamma
    self.patchup_block = patchup_block
    self.dropblock = DropBlock(block_size=drop_block, keep_prob=keep_prob)
    self.conv1 = conv3x3(3, nStages[0], stride=stride)
    self.patchup_0 = PatchUp(block_size=self.patchup_block, gamma=self.gamma)
    self.layer1 = self._wide_layer(wide_basic, nStages[1], n, stride=1)
    self.patchup_1 = PatchUp(block_size=self.patchup_block, gamma=self.gamma)
    self.layer2 = self._wide_layer(wide_basic, nStages[2], n, stride=2)
    self.patchup_2 = PatchUp(block_size=5, gamma=self.gamma)
    self.layer3 = self._wide_layer(wide_basic, nStages[3], n, stride=2)
    self.bn1 = nn.BatchNorm2d(nStages[3], momentum=0.9)
    self.patchup_3 = PatchUp(block_size=3, gamma=self.gamma)
    self.linear = nn.Linear(nStages[3], num_classes)
