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


def compute_grid_offsets(self, grid_size, img_dim, cuda=True, Half=False):
    self.grid_size = grid_size
    g = self.grid_size
    FloatTensor = (torch.cuda.FloatTensor if cuda else torch.FloatTensor)
    FloatTensor = (torch.cuda.HalfTensor if Half else torch.cuda.FloatTensor)
    self.img_dim = img_dim
    self.stride = (self.img_dim / self.grid_size)
    self.grid_x = torch.arange(g).repeat(g, 1).view([1, 1, g, g]).type(FloatTensor)
    self.grid_y = torch.arange(g).repeat(g, 1).t().view([1, 1, g, g]).type(FloatTensor)
    self.scaled_anchors = FloatTensor([((a_w / self.stride), (a_h / self.stride)) for (a_w, a_h) in self.anchors])
    self.anchor_w = self.scaled_anchors[(:, 0)].view((1, self.num_anchors, 1, 1))
    self.anchor_h = self.scaled_anchors[(:, 1)].view((1, self.num_anchors, 1, 1))
