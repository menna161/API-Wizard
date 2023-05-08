import os, sys
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
from modules.patchup import PatchUp, PatchUpMode
from modules.drop_block import DropBlock
from utility.utils import to_one_hot
from modules.mixup import mixup_process, get_lambda
from modules.cutmix import CutMix
from data_loader import per_image_standardization
import random


def __init__(self, block, num_blocks, initial_channels, num_classes, per_img_std=False, stride=1, drop_block=7, keep_prob=0.9, gamma=0.9, patchup_block=7):
    super(PreActResNet, self).__init__()
    self.in_planes = initial_channels
    self.num_classes = num_classes
    self.per_img_std = per_img_std
    self.keep_prob = keep_prob
    self.gamma = gamma
    self.patchup_block = patchup_block
    self.dropblock = DropBlock(block_size=drop_block, keep_prob=keep_prob)
    self.conv1 = nn.Conv2d(3, initial_channels, kernel_size=3, stride=stride, padding=1, bias=False)
    self.patchup_0 = PatchUp(block_size=self.patchup_block, gamma=self.gamma)
    self.layer1 = self._make_layer(block, initial_channels, num_blocks[0], stride=1)
    self.patchup_1 = PatchUp(block_size=self.patchup_block, gamma=self.gamma)
    self.layer2 = self._make_layer(block, (initial_channels * 2), num_blocks[1], stride=2)
    self.patchup_2 = PatchUp(block_size=5, gamma=self.gamma)
    self.layer3 = self._make_layer(block, (initial_channels * 4), num_blocks[2], stride=2)
    self.patchup_3 = PatchUp(block_size=3, gamma=self.gamma)
    self.layer4 = self._make_layer(block, (initial_channels * 8), num_blocks[3], stride=2)
    self.patchup_4 = PatchUp(block_size=3, gamma=self.gamma)
    self.linear = nn.Linear(((initial_channels * 8) * block.expansion), num_classes)
