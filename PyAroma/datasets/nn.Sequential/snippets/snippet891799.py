from __future__ import absolute_import, division, print_function, unicode_literals
import copy
import json
import logging
import math
import os
import shutil
import tarfile
import tempfile
import sys
from io import open
import torch
from torch import nn
from torch.nn import CrossEntropyLoss
from .file_utils import cached_path
from apex.normalization.fused_layer_norm import FusedLayerNorm as BertLayerNorm
import re
import numpy as np
import tensorflow as tf


def __init__(self, config, num_choices, mlp_hidden_dim, mlp_dropout):
    super(BertForMultipleChoiceExtraction, self).__init__(config)
    self.num_choices = num_choices
    self.bert = BertModel(config)
    self.dropout = nn.Dropout(config.hidden_dropout_prob)
    self.classifier = nn.Linear(config.hidden_size, 1)
    self.mlp_classifier = nn.Sequential(nn.Linear(config.hidden_size, (mlp_hidden_dim * 2)), nn.BatchNorm1d((mlp_hidden_dim * 2)), nn.LeakyReLU(), nn.Dropout(mlp_dropout), nn.Linear((mlp_hidden_dim * 2), 1), nn.Sigmoid())
    self.apply(self.init_bert_weights)
