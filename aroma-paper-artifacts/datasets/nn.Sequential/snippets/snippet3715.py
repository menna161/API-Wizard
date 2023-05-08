import numpy as np
from numpy import linalg as la
import math
import logging
import json
import torch
from torch import nn
from torch.nn import init
import torch.nn.functional as F
from torch.autograd import Variable
import nn as mynn
from core.config import cfg
from modeling_rel.sparse_targets_rel import FrequencyBias
from modeling_rel.draw_rectangles.draw_rectangles import draw_union_boxes


def __init__(self, dim_in):
    super().__init__()
    self.dim_in = dim_in
    self.conv = nn.Sequential(nn.Conv2d(2, (dim_in // 2), kernel_size=7, stride=2, padding=3, bias=True), nn.ReLU(inplace=True), nn.BatchNorm2d((dim_in // 2), momentum=0.01), nn.MaxPool2d(kernel_size=3, stride=2, padding=1), nn.Conv2d((dim_in // 2), dim_in, kernel_size=3, stride=1, padding=1, bias=True), nn.ReLU(inplace=True), nn.BatchNorm2d(dim_in, momentum=0.01))
