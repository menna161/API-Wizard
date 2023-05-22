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


def __init__(self, sent_dim, sent_hidden_dim, concept_dim, graph_hidden_dim, graph_output_dim, pretrained_concept_emd, dropout=0.3):
    super(GCN_Sent, self).__init__()
    self.graph_encoder = GCN_Encoder(concept_dim, graph_hidden_dim, graph_output_dim, pretrained_concept_emd)
    self.sent_dim = sent_dim
    self.sent_hidden = sent_hidden_dim
    self.MLP = nn.Sequential(nn.Linear((self.sent_dim + graph_output_dim), (self.sent_hidden * 4)), nn.BatchNorm1d((self.sent_hidden * 4)), nn.ReLU(), nn.Dropout(dropout), nn.Linear((self.sent_hidden * 4), self.sent_hidden), nn.BatchNorm1d(self.sent_hidden), nn.ReLU(), nn.Dropout(dropout), nn.Linear(self.sent_hidden, 1), nn.Sigmoid())
