import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as torch_models
import numpy as np


def __init__(self, dim, num_class, way=None, shots=None, num_fake_novel_class=16):
    super().__init__()
    weight_base = torch.FloatTensor(num_class, dim).normal_(0.0, np.sqrt((2.0 / dim)))
    self.weight_base = nn.Parameter(weight_base, requires_grad=True)
    scale_cls = 10.0
    self.scale_cls = nn.Parameter(torch.FloatTensor(1).fill_(scale_cls), requires_grad=True)
    self.scale_cls_att = nn.Parameter(torch.FloatTensor(1).fill_(scale_cls), requires_grad=True)
    self.phi_avg = nn.Parameter(torch.FloatTensor(dim).fill_(1), requires_grad=True)
    self.phi_att = nn.Parameter(torch.FloatTensor(dim).fill_(1), requires_grad=True)
    self.phi_q = nn.Linear(dim, dim)
    self.phi_q.weight.data.copy_((torch.eye(dim, dim) + (torch.randn(dim, dim) * 0.001)))
    self.phi_q.bias.data.zero_()
    weight_keys = torch.FloatTensor(num_class, dim).normal_(0.0, np.sqrt((2.0 / dim)))
    self.weight_keys = nn.Parameter(weight_keys, requires_grad=True)
    self.dim = dim
    self.num_class = num_class
    self.num_fake_novel_class = num_fake_novel_class
    self.way = way
    self.shots = shots
