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


def __init__(self, *args, **kwargs):
    super(RelPartialLearnableMultiHeadAttn, self).__init__(*args, **kwargs)
    self.r_net = nn.Linear(self.d_model, (self.n_head * self.d_head), bias=False)
