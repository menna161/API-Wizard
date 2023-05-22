import torch
import torch.nn as nn


def __init__(self, in_ch, hidden_ch=6, node_size=(32, 32), add_diag=True, dropout=0.2):
    super(SCG_block, self).__init__()
    self.node_size = node_size
    self.hidden = hidden_ch
    self.nodes = (node_size[0] * node_size[1])
    self.add_diag = add_diag
    self.pool = nn.AdaptiveAvgPool2d(node_size)
    self.mu = nn.Sequential(nn.Conv2d(in_ch, hidden_ch, 3, padding=1, bias=True), nn.Dropout(dropout))
    self.logvar = nn.Sequential(nn.Conv2d(in_ch, hidden_ch, 1, 1, bias=True), nn.Dropout(dropout))
