import torch.nn as nn
import torch
import torch.nn.functional as F
from ltr.models.layers.blocks import conv_block
import ltr.models.layers.filter as filter_layer
from ltr.models.layers.distance import DistanceMap
import math
from pytracking.libs import dcf, fourier, complex
import ltr.models.loss as ltr_losses


def __init__(self, num_iter=1, filter_size=1, feature_dim=256, feat_stride=16, init_step_length=1.0, init_filter_reg=0.01, init_gauss_sigma=1.0, num_dist_bins=5, bin_displacement=1.0, mask_init_factor=4.0, test_loss=None):
    super().__init__()
    if (test_loss is None):
        test_loss = ltr_losses.LBHinge(threshold=0.05)
    self.log_step_length = nn.Parameter((math.log(init_step_length) * torch.ones(1)))
    self.num_iter = num_iter
    self.test_loss = test_loss
    self.filter_reg = nn.Parameter((init_filter_reg * torch.ones(1)))
    self.feat_stride = feat_stride
    self.distance_map = DistanceMap(num_dist_bins, bin_displacement)
    d = (torch.arange(num_dist_bins, dtype=torch.float32).view(1, (- 1), 1, 1) * bin_displacement)
    if (init_gauss_sigma == 0):
        init_gauss = torch.zeros_like(d)
        init_gauss[(0, 0, 0, 0)] = 1
    else:
        init_gauss = torch.exp((((- 1) / 2) * ((d / init_gauss_sigma) ** 2)))
    self.label_map_predictor = nn.Conv2d(num_dist_bins, 1, kernel_size=1, bias=False)
    self.label_map_predictor.weight.data = (init_gauss - init_gauss.min())
    self.target_mask_predictor = nn.Sequential(nn.Conv2d(num_dist_bins, 1, kernel_size=1, bias=False), nn.Sigmoid())
    self.target_mask_predictor[0].weight.data = (mask_init_factor * torch.tanh((2.0 - d)))
    self.spatial_weight_predictor = nn.Conv2d(num_dist_bins, 1, kernel_size=1, bias=False)
    self.spatial_weight_predictor.weight.data.fill_(1.0)
