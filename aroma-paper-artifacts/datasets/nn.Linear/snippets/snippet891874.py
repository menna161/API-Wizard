import collections
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
import torch.nn as nn
from torch.nn import CrossEntropyLoss
from torch.nn.parameter import Parameter
from .file_utils import cached_path
from .modeling import BertLayerNorm as LayerNorm
import re
import numpy as np


def init_weights(self, module):
    ' Initialize the weights.\n        '
    if isinstance(module, (nn.Linear, nn.Embedding)):
        module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)
    elif isinstance(module, LayerNorm):
        module.bias.data.zero_()
        module.weight.data.fill_(1.0)
    if (isinstance(module, nn.Linear) and (module.bias is not None)):
        module.bias.data.zero_()
