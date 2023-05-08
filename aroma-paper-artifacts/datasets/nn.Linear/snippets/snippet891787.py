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


def init_bert_weights(self, module):
    ' Initialize the weights.\n        '
    if isinstance(module, (nn.Linear, nn.Embedding)):
        module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)
    elif isinstance(module, BertLayerNorm):
        module.bias.data.zero_()
        module.weight.data.fill_(1.0)
    if (isinstance(module, nn.Linear) and (module.bias is not None)):
        module.bias.data.zero_()
