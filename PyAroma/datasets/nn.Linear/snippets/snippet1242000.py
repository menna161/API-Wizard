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
    super(SequenceSummary, self).__init__()
    self.summary_type = (config.summary_type if hasattr(config, 'summary_use_proj') else 'last')
    if (self.summary_type == 'attn'):
        raise NotImplementedError
    self.summary = Identity()
    if (hasattr(config, 'summary_use_proj') and config.summary_use_proj):
        if (hasattr(config, 'summary_proj_to_labels') and config.summary_proj_to_labels and (config.num_labels > 0)):
            num_classes = config.num_labels
        else:
            num_classes = config.hidden_size
        self.summary = nn.Linear(config.hidden_size, num_classes)
    self.activation = Identity()
    if (hasattr(config, 'summary_activation') and (config.summary_activation == 'tanh')):
        self.activation = nn.Tanh()
    self.first_dropout = Identity()
    if (hasattr(config, 'summary_first_dropout') and (config.summary_first_dropout > 0)):
        self.first_dropout = nn.Dropout(config.summary_first_dropout)
    self.last_dropout = Identity()
    if (hasattr(config, 'summary_last_dropout') and (config.summary_last_dropout > 0)):
        self.last_dropout = nn.Dropout(config.summary_last_dropout)
