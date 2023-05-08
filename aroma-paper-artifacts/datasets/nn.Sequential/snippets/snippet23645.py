import torch
from torch import nn
import torch.nn.functional as nnFunction


def __init__(self, n_feature, n_hidden, n_output):
    super(OneLayer, self).__init__()
    self.hidden_layer = nn.Sequential(nn.Linear(n_feature, n_hidden), nn.ReLU(True))
    self.predict_layer = nn.Linear(n_hidden, n_output)
