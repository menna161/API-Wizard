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
    super(AlbertPredictionHeadTransform, self).__init__()
    self.dense = nn.Linear(config.hidden_size, config.embedding_size)
    if (isinstance(config.hidden_act, str) or ((sys.version_info[0] == 2) and isinstance(config.hidden_act, unicode))):
        self.transform_act_fn = ACT2FN[config.hidden_act]
    else:
        self.transform_act_fn = config.hidden_act
    self.LayerNorm = AlbertLayerNorm(config.embedding_size, eps=config.layer_norm_eps)
