import torch
import torch.nn as nn
import torch.nn.functional as F
import dgl
import dgl.function as fn
import numpy as np
from torch.nn import init
from torch.autograd import Variable
import torch.autograd as autograd
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import json
from dgl import DGLGraph
import random


def __init__(self, in_feats, out_feats, activation):
    super(NodeApplyModule, self).__init__()
    self.linear = nn.Linear(in_feats, out_feats)
    self.activation = activation
