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
    super(OpenAIGPTLMHeadModel, self).__init__(config)
    self.transformer = OpenAIGPTModel(config)
    self.lm_head = OpenAIGPTLMHead(self.transformer.tokens_embed.weight, config)
    self.apply(self.init_weights)
