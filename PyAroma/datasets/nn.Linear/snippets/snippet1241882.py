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
    super(AlbertEmbeddings, self).__init__()
    self.word_embeddings = nn.Embedding(config.vocab_size, config.embedding_size, padding_idx=0)
    self.word_embeddings_2 = nn.Linear(config.embedding_size, config.hidden_size, bias=False)
    self.position_embeddings = nn.Embedding(config.max_position_embeddings, config.hidden_size)
    self.token_type_embeddings = nn.Embedding(config.type_vocab_size, config.hidden_size)
    self.LayerNorm = AlbertLayerNorm(config.hidden_size, eps=config.layer_norm_eps)
    self.dropout = nn.Dropout(config.hidden_dropout_prob)
