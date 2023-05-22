from __future__ import print_function
import torch
import torch.backends.cudnn as cudnn
import numpy as np
import cv2
import os
import pandas as pd
import copy
import time
import torchvision
from face_detect_lib.models.retinaface import RetinaFace
from face_detect_lib.layers.functions.prior_box import PriorBox
from face_detect_lib.utils.box_utils import decode_batch, decode_landm_batch, decode, decode_landm
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from functools import partial
import torch.nn.functional as F
import torch.utils.model_zoo as model_zoo
from torch.nn import init
import torch.nn as nn
import math
import re
import math
import collections
from functools import partial
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils import model_zoo
import torch.nn.functional as F
import torch.utils.model_zoo as model_zoo
from torch.nn import init
import torch.nn as nn
import math
import torch
import torchvision.models.resnet as resnet


def __init__(self, num_classes=2, bypass_last_bn=False):
    ' Constructor\n        Args:\n            num_classes: number of classes\n        '
    global bypass_bn_weight_list
    bypass_bn_weight_list = []
    self.inplanes = 64
    super(xception, self).__init__()
    self.num_classes = num_classes
    self.conv1 = nn.Conv2d(3, 32, 3, 2, 0, bias=False)
    self.bn1 = nn.BatchNorm2d(32)
    self.relu = nn.ReLU(inplace=True)
    self.conv2 = nn.Conv2d(32, 64, 3, bias=False)
    self.bn2 = nn.BatchNorm2d(64)
    self.block1 = Block(64, 128, 2, 2, start_with_relu=False, grow_first=True)
    self.block2 = Block(128, 256, 2, 2, start_with_relu=True, grow_first=True)
    self.block3 = Block(256, 728, 2, 2, start_with_relu=True, grow_first=True)
    self.block4 = Block(728, 728, 3, 1, start_with_relu=True, grow_first=True)
    self.block5 = Block(728, 728, 3, 1, start_with_relu=True, grow_first=True)
    self.block6 = Block(728, 728, 3, 1, start_with_relu=True, grow_first=True)
    self.block7 = Block(728, 728, 3, 1, start_with_relu=True, grow_first=True)
    self.block8 = Block(728, 728, 3, 1, start_with_relu=True, grow_first=True)
    self.block9 = Block(728, 728, 3, 1, start_with_relu=True, grow_first=True)
    self.block10 = Block(728, 728, 3, 1, start_with_relu=True, grow_first=True)
    self.block11 = Block(728, 728, 3, 1, start_with_relu=True, grow_first=True)
    self.block12 = Block(728, 1024, 2, 2, start_with_relu=True, grow_first=False)
    self.conv3 = SeparableConv2d(1024, 1536, 3, 1, 1)
    self.bn3 = nn.BatchNorm2d(1536)
    self.conv4 = SeparableConv2d(1536, 2048, 3, 1, 1)
    self.bn4 = nn.BatchNorm2d(2048)
    self.fc = nn.Linear(2048, num_classes)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
    if bypass_last_bn:
        for param in bypass_bn_weight_list:
            param.data.zero_()
        print('bypass {} bn.weight in BottleneckBlocks'.format(len(bypass_bn_weight_list)))
