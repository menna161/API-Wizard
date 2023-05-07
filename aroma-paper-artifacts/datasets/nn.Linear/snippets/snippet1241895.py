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
    super(AlbertLMPredictionHead, self).__init__()
    self.transform = BertPredictionHeadTransform(config)
    self.project_layer = nn.Linear(config.hidden_size, config.embedding_size, bias=False)
    self.decoder = nn.Linear(config.embedding_size, config.vocab_size, bias=False)
    self.bias = nn.Parameter(torch.zeros(config.vocab_size))
