import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, num_classes, feat_dim=2048):
    super(CenterLoss, self).__init__()
    self.num_classes = num_classes
    self.feat_dim = feat_dim
    self.centers = nn.Parameter(torch.randn(self.num_classes, self.feat_dim))
