import torch
import math
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from torch.nn.init import xavier_normal_


def forward(self, embedding, e1, rel):
    batch_size = e1.shape[0]
    e1_embedded = embedding[e1].squeeze()
    rel_embedded = self.w_relation(rel).squeeze()
    e1_embedded = self.inp_drop(e1_embedded)
    rel_embedded = self.inp_drop(rel_embedded)
    score = torch.mm((e1_embedded * rel_embedded), embedding.t())
    score = F.sigmoid(score)
    return score
