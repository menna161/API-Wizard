from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import os
import torch
from torch import nn
from torch.nn import CrossEntropyLoss, MSELoss
from .modeling_utils import PreTrainedModel, prune_linear_layer
from .configuration_albert import AlbertConfig
from .file_utils import add_start_docstrings
from .modeling_bert import ACT2FN, BertSelfAttention, BertIntermediate, BertPooler, BertPredictionHeadTransform
import re
import numpy as np
import tensorflow as tf


def __init__(self, config):
    super(AlbertOnlyNSPHead, self).__init__()
    self.seq_relationship = nn.Linear(config.hidden_size, 2)
