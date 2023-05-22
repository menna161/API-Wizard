from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import os
import torch
from torch import nn
from torch.nn import CrossEntropyLoss
from torch.nn import functional as F
from .configuration_utils import PretrainedConfig
from .file_utils import cached_path, WEIGHTS_NAME, TF_WEIGHTS_NAME
from torch.nn import Identity


def __init__(self, config):
    super(PoolerEndLogits, self).__init__()
    self.dense_0 = nn.Linear((config.hidden_size * 2), config.hidden_size)
    self.activation = nn.Tanh()
    self.LayerNorm = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)
    self.dense_1 = nn.Linear(config.hidden_size, 1)