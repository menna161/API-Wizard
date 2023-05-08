from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import copy
import json
import logging
import math
import torch
import torch.nn as nn
from torch.nn import CrossEntropyLoss, Dropout, Embedding, Softmax


def Linear(i_dim, o_dim, bias=True):
    m = nn.Linear(i_dim, o_dim, bias)
    nn.init.normal_(m.weight, std=0.02)
    if bias:
        nn.init.constant_(m.bias, 0.0)
    return m
