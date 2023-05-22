from __future__ import division
import datetime
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
from utils.parse_config import *
from utils.utils import build_targets, to_cpu, non_max_suppression
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
import datetime
from torch2trt import torch2trt


def __init__(self, anchors, num_classes, img_dim=416):
    super(YOLOLayer, self).__init__()
    self.anchors = anchors
    self.num_anchors = len(anchors)
    self.num_classes = num_classes
    self.ignore_thres = 0.5
    self.mse_loss = nn.MSELoss()
    self.bce_loss = nn.BCELoss()
    self.obj_scale = 1
    self.noobj_scale = 100
    self.metrics = {}
    self.img_dim = img_dim
    self.grid_size_x = 0
    self.grid_size_y = 0
    self.stride = 0
    self.grid_x = 0
    self.grid_y = 0
    self.scaled_anchors = 0
    self.anchor_w = 0
    self.anchor_h = 0
