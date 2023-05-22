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
    super(AlbertEncoder, self).__init__()
    self.hidden_size = config.hidden_size
    self.embedding_size = config.embedding_size
    self.embedding_hidden_mapping_in = nn.Linear(self.embedding_size, self.hidden_size)
    self.transformer = AlbertTransformer(config)
