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


def set_embeddings_weights(self, model_embeddings_weights):
    embed_shape = model_embeddings_weights.shape
    self.decoder = nn.Linear(embed_shape[1], embed_shape[0], bias=False)
    self.decoder.weight = model_embeddings_weights
