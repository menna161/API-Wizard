import torch
import torch.utils.data
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


def __init__(self, n_vis=784, n_hin=500, k=5):
    '\n        The basic model for VAE\n        Inputs:\n            n_vis : [int] number of visible units;\n            n_hin : [int] number of latent units;\n            k : [int] layers of RBM;\n        '
    super(RBM, self).__init__()
    self.W = nn.Parameter((torch.randn(n_hin, n_vis) * 0.01))
    self.v_bias = nn.Parameter(torch.zeros(n_vis))
    self.h_bias = nn.Parameter(torch.zeros(n_hin))
    self.k = k
