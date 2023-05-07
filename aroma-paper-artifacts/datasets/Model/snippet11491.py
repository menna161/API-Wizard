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
    super(PreTraining, self).__init__()
    self.bert = Model(config)
    self.cls = PreTrainingHeads(config, self.bert.embeddings.word_embeddings.weight)
    self.vocab_size = config.vocab_size
