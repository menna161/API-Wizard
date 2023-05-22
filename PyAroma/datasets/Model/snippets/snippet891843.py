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
import tensorflow as tf


def __init__(self, config):
    super(GPT2DoubleHeadsModel, self).__init__(config)
    self.transformer = GPT2Model(config)
    self.lm_head = GPT2LMHead(self.transformer.wte.weight, config)
    self.multiple_choice_head = GPT2MultipleChoiceHead(config)
    self.apply(self.init_weights)
