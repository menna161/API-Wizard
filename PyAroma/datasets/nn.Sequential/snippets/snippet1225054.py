import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from functools import partial
from collections import OrderedDict
from config import config
from resnet import get_resnet50


def __init__(self, norm_layer, bn_momentum, latent_size=16):
    super(CVAE, self).__init__()
    self.latent_size = latent_size
    self.encoder = nn.Sequential(nn.Conv3d(2, 3, kernel_size=3, padding=1, bias=False), norm_layer(3, momentum=bn_momentum), nn.ReLU(), nn.Conv3d(3, 16, kernel_size=3, padding=1, bias=False), norm_layer(16, momentum=bn_momentum), nn.ReLU(), nn.Conv3d(16, 16, kernel_size=3, padding=1, bias=False), norm_layer(16, momentum=bn_momentum), nn.ReLU(), nn.AvgPool3d(kernel_size=2, stride=2), nn.Conv3d(16, self.latent_size, kernel_size=3, padding=1, bias=False), norm_layer(self.latent_size, momentum=bn_momentum), nn.ReLU(), nn.AvgPool3d(kernel_size=2, stride=2), nn.Conv3d(self.latent_size, self.latent_size, kernel_size=3, padding=1, bias=False), norm_layer(self.latent_size, momentum=bn_momentum), nn.ReLU())
    self.mean = nn.Conv3d(self.latent_size, self.latent_size, kernel_size=1, bias=True)
    self.log_var = nn.Conv3d(self.latent_size, self.latent_size, kernel_size=1, bias=True)
    self.decoder_x = nn.Sequential(nn.Conv3d(1, 3, kernel_size=3, padding=1, bias=False), norm_layer(3, momentum=bn_momentum), nn.ReLU(), nn.Conv3d(3, 16, kernel_size=3, padding=1, bias=False), norm_layer(16, momentum=bn_momentum), nn.ReLU(), nn.Conv3d(16, 16, kernel_size=3, padding=1, bias=False), norm_layer(16, momentum=bn_momentum), nn.ReLU(), nn.AvgPool3d(kernel_size=2, stride=2), nn.Conv3d(16, self.latent_size, kernel_size=3, padding=1, bias=False), norm_layer(self.latent_size, momentum=bn_momentum), nn.ReLU(), nn.AvgPool3d(kernel_size=2, stride=2), nn.Conv3d(self.latent_size, self.latent_size, kernel_size=3, padding=1, bias=False), norm_layer(self.latent_size, momentum=bn_momentum), nn.ReLU())
    self.decoder = nn.Sequential(nn.ConvTranspose3d((self.latent_size * 2), self.latent_size, kernel_size=3, stride=2, padding=1, dilation=1, output_padding=1), norm_layer(self.latent_size, momentum=bn_momentum), nn.ReLU(inplace=False), nn.ConvTranspose3d(self.latent_size, self.latent_size, kernel_size=3, stride=2, padding=1, dilation=1, output_padding=1), norm_layer(self.latent_size, momentum=bn_momentum), nn.ReLU(inplace=False), nn.Dropout3d(0.1), nn.Conv3d(self.latent_size, 2, kernel_size=1, bias=True))
