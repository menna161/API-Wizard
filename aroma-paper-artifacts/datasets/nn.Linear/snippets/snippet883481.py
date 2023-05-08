import torch
import logging
import torch.nn as nn
import torch.nn.functional as functional


def __init__(self, in_size: int, out_size: int, bias: bool=True, dropout: int=0, weight_norm: bool=False):
    'Linear layer with regularization.\n        Args:\n            in_size (int):\n            out_size (int):\n            bias (bool): if False, remove a bias term\n            dropout (float):\n            weight_norm (bool):\n        '
    super(Linear, self).__init__()
    self.dropout_prob = dropout
    self.fc = nn.Linear(in_size, out_size, bias=bias)
    self.dropout = nn.Dropout(p=dropout)
    if weight_norm:
        self.fc = nn.utils.weight_norm(self.fc, name='weight', dim=0)
