import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.models.resnet import Bottleneck, BasicBlock
from operations import *
from collections import defaultdict
import math
import pdb
import torchvision
import time
from dataset import *
from layers import *
from bi_fpn import BiFPN_PRIMITIVES, BiFPN_Neck_From_Genotype
from layers.box_utils import match_anchors, decode, encode
import numbers
from torchvision.ops import roi_align
from collections import OrderedDict
import logging


def __init__(self, input_channels, stack_convs=3):
    super(DeepHead, self).__init__()
    output_channels = input_channels
    self.layers = nn.ModuleList()
    for i in range(stack_convs):
        if (i == 0):
            self.layers.append(nn.Conv2d(input_channels, output_channels, 3, 1, 1))
        else:
            self.layers.append(nn.Sequential(nn.Conv2d(output_channels, output_channels, 3, 1, 1, groups=output_channels), nn.Conv2d(output_channels, output_channels, 1, 1, 0)))
