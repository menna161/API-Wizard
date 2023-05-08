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
    hidden_dim = cfg.FAST_RCNN.CONV_HEAD_DIM
    module_list = []
    for i in range(cfg.FAST_RCNN.NUM_STACKED_CONVS):
        module_list.extend([nn.Conv2d(dim_in, hidden_dim, 3, 1, 1), nn.ReLU(inplace=True)])
        dim_in = hidden_dim
    self.convs = nn.Sequential(*module_list)
    self.dim_out = fc_dim = cfg.FAST_RCNN.MLP_HEAD_DIM
    roi_size = cfg.FAST_RCNN.ROI_XFORM_RESOLUTION
    self.fc = nn.Linear(((dim_in * roi_size) * roi_size), fc_dim)
    self._init_weights()
