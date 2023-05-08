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


def __init__(self, block=Bottleneck, layers=[3, 4, 6, 3], num_classes=400, shortcut_type='B', dropout=0.5, alpha=8, beta=0.125, tau=16, zero_init_residual=False):
    super(SlowFast, self).__init__()
    self.alpha = alpha
    self.beta = beta
    self.tau = tau
    'Fast Network'
    self.fast_inplanes = int((64 * beta))
    fast_inplanes = self.fast_inplanes
    self.fast_conv1 = nn.Conv3d(3, fast_inplanes, kernel_size=(5, 7, 7), stride=(1, 2, 2), padding=(2, 3, 3), bias=False)
    self.fast_bn1 = nn.BatchNorm3d(int((64 * beta)))
    self.fast_relu = nn.ReLU(inplace=True)
    self.fast_maxpool = nn.MaxPool3d(kernel_size=(1, 3, 3), stride=(1, 2, 2), padding=(0, 1, 1))
    self.fast_res1 = self._make_layer_fast(block, int((64 * beta)), layers[0], shortcut_type, head_conv=3)
    self.fast_res2 = self._make_layer_fast(block, int((128 * beta)), layers[1], shortcut_type, stride=2, head_conv=3)
    self.fast_res3 = self._make_layer_fast(block, int((256 * beta)), layers[2], shortcut_type, stride=2, head_conv=3)
    self.fast_res4 = self._make_layer_fast(block, int((512 * beta)), layers[3], shortcut_type, stride=2, head_conv=3)
    'Slow Network'
    self.slow_inplanes = 64
    slow_inplanes = self.slow_inplanes
    self.slow_conv1 = nn.Conv3d(3, slow_inplanes, kernel_size=(1, 7, 7), stride=(1, 2, 2), padding=(0, 3, 3), bias=False)
    self.slow_bn1 = nn.BatchNorm3d(64)
    self.slow_relu = nn.ReLU(inplace=True)
    self.slow_maxpool = nn.MaxPool3d(kernel_size=(1, 3, 3), stride=(1, 2, 2), padding=(0, 1, 1))
    self.slow_res1 = self._make_layer_slow(block, 64, layers[0], shortcut_type, head_conv=1)
    self.slow_res2 = self._make_layer_slow(block, 128, layers[1], shortcut_type, stride=2, head_conv=1)
    self.slow_res3 = self._make_layer_slow(block, 256, layers[2], shortcut_type, stride=2, head_conv=3)
    self.slow_res4 = self._make_layer_slow(block, 512, layers[3], shortcut_type, stride=2, head_conv=3)
    'Lateral Connections'
    self.Tconv1 = nn.Conv3d(int((64 * beta)), int((128 * beta)), kernel_size=(5, 1, 1), stride=(alpha, 1, 1), padding=(2, 0, 0), bias=False)
    self.Tconv2 = nn.Conv3d(int((256 * beta)), int((512 * beta)), kernel_size=(5, 1, 1), stride=(alpha, 1, 1), padding=(2, 0, 0), bias=False)
    self.Tconv3 = nn.Conv3d(int((512 * beta)), int((1024 * beta)), kernel_size=(5, 1, 1), stride=(alpha, 1, 1), padding=(2, 0, 0), bias=False)
    self.Tconv4 = nn.Conv3d(int((1024 * beta)), int((2048 * beta)), kernel_size=(5, 1, 1), stride=(alpha, 1, 1), padding=(2, 0, 0), bias=False)
    self.dp = nn.Dropout(dropout)
    self.fc = nn.Linear((self.fast_inplanes + self.slow_inplanes), num_classes)
    for m in self.modules():
        if isinstance(m, nn.Conv3d):
            m.weight = nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
        elif isinstance(m, nn.BatchNorm3d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
    if zero_init_residual:
        for m in self.modules():
            if isinstance(m, Bottleneck):
                nn.init.constant_(m.bn3.weight, 0)
