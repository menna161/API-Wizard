import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import time
import utils.logger as logger


def __init__(self, rnn_dims, fc_dims, feat_dims, aux_dims):
    super().__init__()
    self.n_classes = 256
    self.rnn_dims = rnn_dims
    self.aux_dims = aux_dims
    self.half_rnn_dims = (rnn_dims // 2)
    self.feat_dims = feat_dims
    self.gru = nn.GRU(((feat_dims + self.aux_dims) + 3), rnn_dims, batch_first=True)
    self.fc1 = nn.Linear((self.half_rnn_dims + self.aux_dims), fc_dims)
    self.fc2 = nn.Linear(fc_dims, self.n_classes)
    self.fc3 = nn.Linear((self.half_rnn_dims + self.aux_dims), fc_dims)
    self.fc4 = nn.Linear(fc_dims, self.n_classes)
    self.register_buffer('mask', self.create_mask())
