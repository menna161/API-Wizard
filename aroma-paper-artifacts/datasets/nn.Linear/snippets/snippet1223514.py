import os
import copy
import warnings
import numpy as np
import pickle
from tqdm import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from torch.utils.data import DataLoader
from torch.optim import Optimizer
from torch_geometric.nn import GATConv
from torch_sparse import SparseTensor
from ...dataloader.graph_data import Graph_Processer
from ..basic_model import Basic_Model
from ...sampler import Basic_Sampler
from ...utils import *
import warnings


def train_one_epoch(self, data, optim: Optimizer, epoch_index, is_sample=False, is_subgraph=False, args=None, is_train=True):
    '\n        Train for one epoch\n        Inputs:\n            dataloader  : Train dataset with form of dataloader\n            optim       : Optimizer for model\n            epoch_index : [int] Current epoch on training stage\n            is_sample   : [bool] Whether sample nodes to compute subgraph likelihood\n            is_subgraph : [bool] Whether sample nodes to update nodes embedding with subgraph\n            args        : Hyper-parameters\n            is_train    : [bool] True or False, whether to update the global params in the probabilistic model\n\n        Attributes:\n            adj_nodes   : Number of nodes in adjacent matrix\n            adj_sum     : Number of non-zero element in adjacent matrix\n\n        '
    if (epoch_index == 0):
        self.num_classes = len(np.unique(data.y.cpu()))
        self.pred_layer = nn.Linear((self._model_setting.hid_dims[(- 1)] + self._model_setting.z_dims[(- 1)]), self.num_classes).to(self._model_setting.device)
        self.adj_nodes = data.x.shape[0]
        self.adj_sum = data.edge_index.shape[1]
        if is_sample:
            self.adj_coo = self.graph_processer.graph_from_edges(edge_index=data.edge_index, n_nodes=self.adj_nodes).tocoo()
            self.num_sample = args.num_sample
            self.alpha = 2.0
            self.measure = 'degree'
            self.prob = self.graph_processer.distribution_from_graph(torch.tensor(self.adj_coo.todense(), dtype=torch.float32), self.alpha, self.measure)
        else:
            self.adj = self.graph_processer.graph_from_edges(edge_index=data.edge_index, n_nodes=self.adj_nodes, to_tensor=True, to_sparse=False)
    if is_subgraph:
        pass
    else:
        return self.train_full_graph(data, optim, epoch_index, is_sample=is_sample, args=args, is_train=is_train)
