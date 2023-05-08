import torch
import torch.nn as nn
import numpy as np
import math


def __init__(self, d_q, d_v, alpha, dropout=0.1):
    super(GraphAttention, self).__init__()
    self.dropout = nn.Dropout(dropout)
    self.attention = nn.Linear((d_q + d_v), 1)
    self.leaky_relu = nn.LeakyReLU(alpha)
