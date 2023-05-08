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


def __init__(self, sent_dim, concept_dim, relation_dim, concept_num, relation_num, qas_encoded_dim, pretrained_concept_emd, pretrained_relation_emd, lstm_dim, lstm_layer_num, device, dropout=0.1, bidirect=True, num_random_paths=None, path_attention=True, qa_attention=True):
    super(KnowledgeEnhancedRelationNetwork, self).__init__()
    self.num_random_paths = num_random_paths
    self.concept_dim = concept_dim
    self.relation_dim = relation_dim
    self.path_attention = path_attention
    self.qa_attention = qa_attention
    self.sent_dim = sent_dim
    self.concept_emd = nn.Embedding(concept_dim, concept_num)
    self.relation_emd = nn.Embedding(relation_num, relation_dim)
    if (pretrained_concept_emd is not None):
        self.concept_emd.weight = nn.Parameter(pretrained_concept_emd)
    else:
        bias = np.sqrt((6.0 / self.concept_dim))
        nn.init.uniform_(self.concept_emd.weight, (- bias), bias)
    if (pretrained_relation_emd is not None):
        self.relation_emd.weight = nn.Parameter(pretrained_relation_emd)
    else:
        bias = np.sqrt((6.0 / self.relation_dim))
        nn.init.uniform_(self.relation_emd.weight, (- bias), bias)
    self.qas_encoded_dim = qas_encoded_dim
    self.lstm = nn.LSTM(input_size=(concept_dim + relation_dim), hidden_size=lstm_dim, num_layers=lstm_layer_num, bidirectional=bidirect, dropout=dropout)
    if bidirect:
        self.lstm_dim = (lstm_dim * 2)
    else:
        self.lstm_dim = lstm_dim
    self.qas_encoder = nn.Sequential(nn.Linear(((2 * concept_dim) + sent_dim), (self.qas_encoded_dim * 2)), nn.Dropout(dropout), nn.LeakyReLU(), nn.Linear((self.qas_encoded_dim * 2), self.qas_encoded_dim), nn.Dropout(dropout), nn.LeakyReLU())
    self.nonlinear = nn.LeakyReLU()
    if self.path_attention:
        self.qas_pathlstm_att = nn.Linear(self.qas_encoded_dim, self.lstm_dim)
        self.qas_pathlstm_att.apply(weight_init)
    if self.qa_attention:
        self.sent_ltrel_att = nn.Linear(sent_dim, self.qas_encoded_dim)
        self.sent_ltrel_att.apply(weight_init)
    self.device = device
    self.hidden2output = nn.Sequential(nn.Linear(((self.qas_encoded_dim + self.lstm_dim) + self.sent_dim), 1), nn.Sigmoid())
    self.lstm.apply(weight_init)
    self.qas_encoder.apply(weight_init)
    self.hidden2output.apply(weight_init)
