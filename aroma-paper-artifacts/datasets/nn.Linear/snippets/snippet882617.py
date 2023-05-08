import torch
import torch.nn as nn
import numpy as np
import copy


def __init__(self, n_head, d_k, d_in):
    super().__init__()
    self.n_head = n_head
    self.d_k = d_k
    self.d_in = d_in
    self.Q = nn.Parameter(torch.zeros((n_head, d_k))).requires_grad_(True)
    nn.init.normal_(self.Q, mean=0, std=np.sqrt((2.0 / d_k)))
    self.fc1_k = nn.Linear(d_in, (n_head * d_k))
    nn.init.normal_(self.fc1_k.weight, mean=0, std=np.sqrt((2.0 / d_k)))
    self.attention = ScaledDotProductAttention(temperature=np.power(d_k, 0.5))
