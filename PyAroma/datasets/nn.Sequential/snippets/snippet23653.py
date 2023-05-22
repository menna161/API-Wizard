import torch
from torch import nn
import torch.nn.functional as nnFunction


def __init__(self, in_dim, n_hidden_1, n_hidden_2, n_hidden_3, n_hidden_4, n_hidden_5, out_dim):
    super(Batch_Net_5, self).__init__()
    self.layer1 = nn.Sequential(nn.Linear(in_dim, n_hidden_1), nn.BatchNorm1d(n_hidden_1), nn.ReLU(True))
    self.layer2 = nn.Sequential(nn.Linear(n_hidden_1, n_hidden_2), nn.BatchNorm1d(n_hidden_2), nn.ReLU(True))
    self.layer3 = nn.Sequential(nn.Linear(n_hidden_2, n_hidden_3), nn.BatchNorm1d(n_hidden_3), nn.ReLU(True))
    self.layer4 = nn.Sequential(nn.Linear(n_hidden_3, n_hidden_4), nn.BatchNorm1d(n_hidden_4), nn.ReLU(True))
    self.layer5 = nn.Sequential(nn.Linear(n_hidden_4, n_hidden_5), nn.BatchNorm1d(n_hidden_5), nn.ReLU(True))
    self.layer6 = nn.Sequential(nn.Linear(n_hidden_5, out_dim))
