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


def __init__(self, config, bert_model_embedding_weights):
    super(BertLMPredictionHead, self).__init__()
    self.transform = BertPredictionHeadTransform(config)
    self.decoder = nn.Linear(bert_model_embedding_weights.size(1), bert_model_embedding_weights.size(0), bias=False)
    self.decoder.weight = bert_model_embedding_weights
    self.bias = nn.Parameter(torch.zeros(bert_model_embedding_weights.size(0)))
