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


def compute_grid_offsets(self, grid_size_y, grid_size_x, img_dim, cuda=True, Half=False):
    self.grid_size_x = grid_size_x
    self.grid_size_y = grid_size_y
    gx = self.grid_size_x
    gy = self.grid_size_y
    FloatTensor = (torch.cuda.FloatTensor if cuda else torch.FloatTensor)
    FloatTensor = (torch.cuda.HalfTensor if Half else torch.cuda.FloatTensor)
    self.img_dim = img_dim
    self.stride = (self.img_dim / max(gx, gy))
    self.grid_x = torch.arange(gx).repeat(gy, 1).view([1, 1, gy, gx]).type(FloatTensor)
    self.grid_y = torch.arange(gy).repeat(gx, 1).t().contiguous().view([1, 1, gy, gx]).type(FloatTensor)
    self.scaled_anchors = FloatTensor([((a_w / self.stride), (a_h / self.stride)) for (a_w, a_h) in self.anchors])
    self.anchor_w = self.scaled_anchors[(:, 0)].view((1, self.num_anchors, 1, 1))
    self.anchor_h = self.scaled_anchors[(:, 1)].view((1, self.num_anchors, 1, 1))
