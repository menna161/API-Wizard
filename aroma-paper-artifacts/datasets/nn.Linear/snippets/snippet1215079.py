from __future__ import print_function
import math
import torch
import torch.nn as nn
from torch.nn.utils.weight_norm import weight_norm
from fc import FCNet
from OT_torch_ import cost_matrix_batch_torch, IPOT_torch_batch_uniform, GW_distance_uniform, IPOT_distance_torch_batch_uniform
import pdb


def __init__(self, v_dim, q_dim, h_dim, h_out, act='ReLU', dropout=[0.2, 0.5], k=3):
    super(BCNet, self).__init__()
    self.lamb = 0.0
    self.c = 32
    self.k = k
    self.v_dim = v_dim
    self.q_dim = q_dim
    self.h_dim = h_dim
    self.h_out = h_out
    self.v_net = FCNet([v_dim, (h_dim * self.k)], act=act, dropout=dropout[0])
    self.q_net = FCNet([q_dim, (h_dim * self.k)], act=act, dropout=dropout[0])
    self.dropout = nn.Dropout(dropout[1])
    if (1 < k):
        self.p_net = nn.AvgPool1d(self.k, stride=self.k)
    if (None == h_out):
        pass
    elif (h_out <= self.c):
        self.h_mat = nn.Parameter(torch.Tensor(1, h_out, 1, (h_dim * self.k)).normal_())
        self.h_bias = nn.Parameter(torch.Tensor(1, h_out, 1, 1).normal_())
    else:
        self.h_net = weight_norm(nn.Linear((h_dim * self.k), h_out), dim=None)
