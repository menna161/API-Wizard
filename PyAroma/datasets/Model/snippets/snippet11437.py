from __future__ import absolute_import, division, print_function
import os
import random
import sys
import unicodedata
import copy
import json
import logging
import math
import collections
from io import open
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset, SequentialSampler
from tqdm import tqdm
from torch.nn import CrossEntropyLoss, Dropout, Embedding, Softmax


def __init__(self, config):
    super(QuestionAnswering, self).__init__()
    self.bert = Model(config)
    self.qa_outputs = Linear(config.hidden_size, 2)
