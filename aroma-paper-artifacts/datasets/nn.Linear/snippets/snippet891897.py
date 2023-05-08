import os
import copy
import json
import math
import logging
import tarfile
import tempfile
import shutil
import collections
import sys
from io import open
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import CrossEntropyLoss
from torch.nn.parameter import Parameter
from .modeling import BertLayerNorm as LayerNorm
from .modeling_transfo_xl_utilities import ProjectedAdaptiveLogSoftmax, sample_logits
from .file_utils import cached_path
import numpy as np
import tensorflow as tf


def __init__(self, d_model, d_inner, dropout, pre_lnorm=False):
    super(PositionwiseFF, self).__init__()
    self.d_model = d_model
    self.d_inner = d_inner
    self.dropout = dropout
    self.CoreNet = nn.Sequential(nn.Linear(d_model, d_inner), nn.ReLU(inplace=True), nn.Dropout(dropout), nn.Linear(d_inner, d_model), nn.Dropout(dropout))
    self.layer_norm = LayerNorm(d_model)
    self.pre_lnorm = pre_lnorm
