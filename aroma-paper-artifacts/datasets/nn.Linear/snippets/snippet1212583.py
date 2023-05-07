import torch
import torch.nn as nn
from onmt.modules.position_ffn import PositionwiseFeedForward


def __init__(self, model_dim, dropout=0.1, aan_useffn=False):
    self.model_dim = model_dim
    self.aan_useffn = aan_useffn
    super(AverageAttention, self).__init__()
    if aan_useffn:
        self.average_layer = PositionwiseFeedForward(model_dim, model_dim, dropout)
    self.gating_layer = nn.Linear((model_dim * 2), (model_dim * 2))
