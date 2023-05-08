import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import numba as nb
import multiprocessing
import torch_scatter


def __init__(self, BEV_net, grid_size, pt_model='pointnet', fea_dim=3, pt_pooling='max', kernal_size=3, out_pt_fea_dim=64, max_pt_per_encode=64, cluster_num=4, pt_selection='farthest', fea_compre=None):
    super(ptBEVnet, self).__init__()
    assert (pt_pooling in ['max'])
    assert (pt_selection in ['random', 'farthest'])
    if (pt_model == 'pointnet'):
        self.PPmodel = nn.Sequential(nn.BatchNorm1d(fea_dim), nn.Linear(fea_dim, 64), nn.BatchNorm1d(64), nn.ReLU(inplace=True), nn.Linear(64, 128), nn.BatchNorm1d(128), nn.ReLU(inplace=True), nn.Linear(128, 256), nn.BatchNorm1d(256), nn.ReLU(inplace=True), nn.Linear(256, out_pt_fea_dim))
    self.pt_model = pt_model
    self.BEV_model = BEV_net
    self.pt_pooling = pt_pooling
    self.max_pt = max_pt_per_encode
    self.pt_selection = pt_selection
    self.fea_compre = fea_compre
    self.grid_size = grid_size
    if (kernal_size != 1):
        if (self.pt_pooling == 'max'):
            self.local_pool_op = torch.nn.MaxPool2d(kernal_size, stride=1, padding=((kernal_size - 1) // 2), dilation=1)
        else:
            raise NotImplementedError
    else:
        self.local_pool_op = None
    if (self.pt_pooling == 'max'):
        self.pool_dim = out_pt_fea_dim
    if (self.fea_compre is not None):
        self.fea_compression = nn.Sequential(nn.Linear(self.pool_dim, self.fea_compre), nn.ReLU())
        self.pt_fea_dim = self.fea_compre
    else:
        self.pt_fea_dim = self.pool_dim
