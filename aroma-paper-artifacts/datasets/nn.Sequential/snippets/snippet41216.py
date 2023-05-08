import torch
import torch.nn as nn
import torch.nn.parallel
from miscc.config import cfg
from miscc.utils import compute_transformation_matrix, compute_transformation_matrix_inverse
from torch.autograd import Variable


def _make_layer(self, block, channel_num):
    layers = []
    for i in range(cfg.GAN.R_NUM):
        layers.append(block(channel_num))
    return nn.Sequential(*layers)
