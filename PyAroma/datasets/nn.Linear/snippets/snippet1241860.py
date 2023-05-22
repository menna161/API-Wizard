from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import math
import os
import sys
import torch
from torch import nn
from torch.nn import CrossEntropyLoss, MSELoss
from .modeling_utils import PreTrainedModel, prune_linear_layer
from .configuration_albert import AlbertConfig
from .file_utils import add_start_docstrings
import re
import numpy as np
import tensorflow as tf


def _init_weights(self, module):
    ' Initialize the weights '
    if isinstance(module, (nn.Linear, nn.Embedding)):
        module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)
    elif isinstance(module, AlbertLayerNorm):
        module.bias.data.zero_()
        module.weight.data.fill_(1.0)
    if (isinstance(module, nn.Linear) and (module.bias is not None)):
        module.bias.data.zero_()
