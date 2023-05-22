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
    super(AlbertIntermediate, self).__init__()
    self.dense = nn.Linear(config.hidden_size, config.intermediate_size)
    self.output = AlbertOutput(config)
    if (isinstance(config.hidden_act, str) or ((sys.version_info[0] == 2) and isinstance(config.hidden_act, unicode))):
        self.intermediate_act_fn = ACT2FN[config.hidden_act]
    else:
        self.intermediate_act_fn = config.hidden_act