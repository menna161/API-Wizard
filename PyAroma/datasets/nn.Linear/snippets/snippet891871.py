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


def __init__(self, config):
    super(OpenAIGPTMultipleChoiceHead, self).__init__()
    self.n_embd = config.n_embd
    self.dropout = nn.Dropout2d(config.resid_pdrop)
    self.linear = nn.Linear(config.n_embd, 1)
    nn.init.normal_(self.linear.weight, std=0.02)
    nn.init.normal_(self.linear.bias, 0)
