import torch
from collections import OrderedDict
from torch.nn import functional as F
import numpy as np
from model import WideAndDeepModel


def __init__(self, col_names, max_ids, embed_dim, mlp_dims, dropout, use_cuda, local_lr, global_lr, weight_decay, base_model_name, num_expert, num_output):
    super(MetaModel, self).__init__()
    if (base_model_name == 'WD'):
        self.model = WideAndDeepModel(col_names=col_names, max_ids=max_ids, embed_dim=embed_dim, mlp_dims=mlp_dims, dropout=dropout, use_cuda=use_cuda, num_expert=num_expert, num_output=num_output)
    self.local_lr = local_lr
    self.criterion = torch.nn.BCELoss()
    self.meta_optimizer = torch.optim.Adam(params=self.model.parameters(), lr=global_lr, weight_decay=weight_decay)
