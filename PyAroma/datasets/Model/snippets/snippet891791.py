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


def __init__(self, config):
    super(BertForPreTraining, self).__init__(config)
    self.bert = BertModel(config)
    self.cls = BertPreTrainingHeads(config, self.bert.embeddings.word_embeddings.weight)
    self.apply(self.init_bert_weights)
