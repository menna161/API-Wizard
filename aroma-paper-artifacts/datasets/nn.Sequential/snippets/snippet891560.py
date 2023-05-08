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


def __init__(self, concept_dim, concept_num, pretrained_concept_emd, sent_dim, latent_rel_dim, device):
    super(RelationNetwork, self).__init__()
    self.concept_dim = concept_dim
    self.sent_dim = sent_dim
    self.concept_emd = nn.Embedding(concept_dim, concept_num)
    if (pretrained_concept_emd is not None):
        self.concept_emd.weight = nn.Parameter(pretrained_concept_emd)
    else:
        bias = np.sqrt((6.0 / self.concept_dim))
        nn.init.uniform_(self.concept_emd.weight, (- bias), bias)
    self.latent_rel_dim = latent_rel_dim
    self.device = device
    self.relation_extractor = nn.Sequential(nn.Linear(((2 * concept_dim) + sent_dim), (self.latent_rel_dim * 2)), nn.ReLU(), nn.BatchNorm1d((self.latent_rel_dim * 2)), nn.Linear((self.latent_rel_dim * 2), self.latent_rel_dim), nn.BatchNorm1d(self.latent_rel_dim), nn.ReLU())
    self.hidden2output = nn.Sequential(nn.Linear(latent_rel_dim, 1), nn.Sigmoid())
