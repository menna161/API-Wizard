from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import math
import os
import sys
import torch
from torch import nn
from torch.nn import CrossEntropyLoss, MSELoss
from .modeling_utils import PreTrainedModel, prune_linear_layer
from .configuration_albert import AlbertConfig
from .file_utils import add_start_docstrings
import re
import numpy as np
import tensorflow as tf


def __init__(self, config):
    super(AlbertSelfAttention, self).__init__()
    if ((config.hidden_size % config.num_attention_heads) != 0):
        raise ValueError(('The hidden size (%d) is not a multiple of the number of attention heads (%d)' % (config.hidden_size, config.num_attention_heads)))
    self.output_attentions = config.output_attentions
    self.num_attention_heads = config.num_attention_heads
    self.attention_head_size = int((config.hidden_size / config.num_attention_heads))
    self.all_head_size = (self.num_attention_heads * self.attention_head_size)
    self.query = nn.Linear(config.hidden_size, self.all_head_size)
    self.key = nn.Linear(config.hidden_size, self.all_head_size)
    self.value = nn.Linear(config.hidden_size, self.all_head_size)
    self.dropout = nn.Dropout(config.attention_probs_dropout_prob)
