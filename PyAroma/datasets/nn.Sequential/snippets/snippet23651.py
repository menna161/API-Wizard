import torch
from torch import nn
import torch.nn.functional as nnFunction


def __init__(self, in_dim, n_hidden_1, n_hidden_2, out_dim):
    super(Batch_Net, self).__init__()
    self.layer1 = nn.Sequential(nn.Linear(in_dim, n_hidden_1), nn.BatchNorm1d(n_hidden_1), nn.ReLU(True))
    self.layer2 = nn.Sequential(nn.Linear(n_hidden_1, n_hidden_2), nn.BatchNorm1d(n_hidden_2), nn.ReLU(True))
    self.layer3 = nn.Sequential(nn.Linear(n_hidden_2, out_dim))
