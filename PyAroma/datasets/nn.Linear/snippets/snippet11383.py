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


def Linear(i_dim, o_dim, bias=True):
    m = nn.Linear(i_dim, o_dim, bias)
    nn.init.normal_(m.weight, std=0.02)
    if bias:
        nn.init.constant_(m.bias, 0.0)
    return m
