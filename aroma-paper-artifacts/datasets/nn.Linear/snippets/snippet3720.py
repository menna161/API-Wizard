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


def __init__(self, dim_in, roi_xform_func, spatial_scale):
    super().__init__()
    self.dim_in = dim_in
    self.roi_xform = roi_xform_func
    self.spatial_scale = spatial_scale
    self.dim_out = hidden_dim = cfg.FAST_RCNN.MLP_HEAD_DIM
    roi_size = cfg.FAST_RCNN.ROI_XFORM_RESOLUTION
    self.fc1 = nn.Linear((dim_in * (roi_size ** 2)), hidden_dim)
    self.fc2 = nn.Linear(hidden_dim, hidden_dim)
    self._init_weights()
