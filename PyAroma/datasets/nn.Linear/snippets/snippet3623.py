import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as init
from torch.autograd import Variable
from core.config import cfg
import nn as mynn
import utils.net as net_utils


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
