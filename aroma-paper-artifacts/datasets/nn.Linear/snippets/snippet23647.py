import torch
from torch import nn
import torch.nn.functional as nnFunction


def __init__(self, in_dim, n_hidden_1, n_hidden_2, out_dim):
    super(simpleNet, self).__init__()
    self.layer1 = nn.Linear(in_dim, n_hidden_1)
    self.layer2 = nn.Linear(n_hidden_1, n_hidden_2)
    self.layer3 = nn.Linear(n_hidden_2, out_dim)
