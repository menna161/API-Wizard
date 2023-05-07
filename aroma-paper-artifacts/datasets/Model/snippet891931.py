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


def __init__(self, config):
    super(TransfoXLLMHeadModel, self).__init__(config)
    self.transformer = TransfoXLModel(config)
    self.sample_softmax = config.sample_softmax
    if (config.sample_softmax > 0):
        self.out_layer = nn.Linear(config.d_model, config.n_token)
        self.sampler = LogUniformSampler(config.n_token, config.sample_softmax)
    else:
        self.crit = ProjectedAdaptiveLogSoftmax(config.n_token, config.d_embed, config.d_model, config.cutoffs, div_val=config.div_val)
    self.apply(self.init_weights)
    self.tie_weights()
