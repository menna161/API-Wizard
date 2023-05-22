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


def __init__(self, in_filters, out_filters, reps, strides=1, start_with_relu=True, grow_first=True):
    super(Block, self).__init__()
    if ((out_filters != in_filters) or (strides != 1)):
        self.skip = nn.Conv2d(in_filters, out_filters, 1, stride=strides, bias=False)
        self.skipbn = nn.BatchNorm2d(out_filters)
    else:
        self.skip = None
    self.relu = nn.ReLU(inplace=True)
    rep = []
    filters = in_filters
    if grow_first:
        rep.append(self.relu)
        rep.append(SeparableConv2d(in_filters, out_filters, 3, stride=1, padding=1, bias=False))
        rep.append(nn.BatchNorm2d(out_filters))
        filters = out_filters
    for i in range((reps - 1)):
        rep.append(self.relu)
        rep.append(SeparableConv2d(filters, filters, 3, stride=1, padding=1, bias=False))
        rep.append(nn.BatchNorm2d(filters))
    if (not grow_first):
        rep.append(self.relu)
        rep.append(SeparableConv2d(in_filters, out_filters, 3, stride=1, padding=1, bias=False))
        rep.append(nn.BatchNorm2d(out_filters))
    if (not start_with_relu):
        rep = rep[1:]
    else:
        rep[0] = nn.ReLU(inplace=False)
    if (strides != 1):
        rep.append(nn.MaxPool2d(3, strides, 1))
    self.rep = nn.Sequential(*rep)
