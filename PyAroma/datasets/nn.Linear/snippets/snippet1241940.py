from __future__ import absolute_import, division, print_function, unicode_literals
import json
import logging
import math
import os
import sys
from io import open
import torch
from torch import nn
from torch.nn import CrossEntropyLoss, MSELoss
from .modeling_utils import PreTrainedModel, prune_linear_layer
from .configuration_bert import BertConfig
from .file_utils import add_start_docstrings
import re
import numpy as np
import tensorflow as tf


def __init__(self, config):
    super(BertOutput, self).__init__()
    self.dense = nn.Linear(config.intermediate_size, config.hidden_size)
    self.LayerNorm = BertLayerNorm(config.hidden_size, eps=config.layer_norm_eps)
    self.dropout = nn.Dropout(config.hidden_dropout_prob)
