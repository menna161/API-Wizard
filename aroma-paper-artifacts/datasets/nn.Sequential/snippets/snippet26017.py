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


def _make_layer_slow(self, block, planes, blocks, shortcut_type, stride=1, head_conv=1):
    downsample = None
    if ((stride != 1) or ((self.slow_inplanes + (int((self.slow_inplanes * self.beta)) * 2)) != (planes * block.expansion))):
        if (shortcut_type == 'A'):
            downsample = partial(downsample_basic_block, planes=(planes * block.expansion), stride=stride)
        else:
            downsample = nn.Sequential(nn.Conv3d((self.slow_inplanes + (int((self.slow_inplanes * self.beta)) * 2)), (planes * block.expansion), kernel_size=1, stride=(1, stride, stride), bias=False))
    layers = []
    layers.append(block((self.slow_inplanes + (int((self.slow_inplanes * self.beta)) * 2)), planes, stride, downsample, head_conv=head_conv))
    self.slow_inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.slow_inplanes, planes, head_conv=head_conv))
    return nn.Sequential(*layers)
