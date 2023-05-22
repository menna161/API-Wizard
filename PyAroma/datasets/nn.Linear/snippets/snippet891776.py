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
    super(BertPredictionHeadTransform, self).__init__()
    self.dense = nn.Linear(config.hidden_size, config.hidden_size)
    if (isinstance(config.hidden_act, str) or ((sys.version_info[0] == 2) and isinstance(config.hidden_act, unicode))):
        self.transform_act_fn = ACT2FN[config.hidden_act]
    else:
        self.transform_act_fn = config.hidden_act
    self.LayerNorm = BertLayerNorm(config.hidden_size, eps=1e-12)
