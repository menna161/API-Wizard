import torch
import torch.nn as nn
from torch.autograd.function import Function
import pdb


def __init__(self, num_classes, feat_dim, size_average=True):
    super(DiscCentroidsLoss, self).__init__()
    self.num_classes = num_classes
    self.centroids = nn.Parameter(torch.randn(num_classes, feat_dim))
    self.disccentroidslossfunc = DiscCentroidsLossFunc.apply
    self.feat_dim = feat_dim
    self.size_average = size_average
