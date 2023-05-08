import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import BertModel
from common import *


def __init__(self, n_h=256, n_feats=6, n_bert=768, dropout=0.2):
    super().__init__()
    n_x = (n_feats + (2 * n_bert))
    self.lin = lin_layer(n_in=n_x, n_out=n_h, dropout=dropout)
    self.lin_q = lin_layer(n_in=(n_feats + n_bert), n_out=n_h, dropout=dropout)
    self.lin_a = lin_layer(n_in=(n_feats + n_bert), n_out=n_h, dropout=dropout)
    self.head_q = nn.Linear((2 * n_h), N_Q_TARGETS)
    self.head_a = nn.Linear((2 * n_h), N_A_TARGETS)
