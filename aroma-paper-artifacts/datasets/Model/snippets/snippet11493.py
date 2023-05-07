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


def __init__(self, config):
    super(QuestionAnswering, self).__init__()
    self.bert = Model(config)
    self.qa_outputs = Linear(config.hidden_size, 2)
