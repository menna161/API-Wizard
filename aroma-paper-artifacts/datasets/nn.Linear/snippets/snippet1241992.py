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
    super(PoolerStartLogits, self).__init__()
    self.dense = nn.Linear(config.hidden_size, 1)
