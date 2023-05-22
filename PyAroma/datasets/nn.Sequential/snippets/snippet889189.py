import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


def __init__(self, col_names, max_ids, embed_dim, mlp_dims, dropout, use_cuda, num_expert, num_output):
    super().__init__()
    self.embedding = Emb(col_names, max_ids, embed_dim, use_cuda)
    self.embed_output_dim = ((len(col_names['static']) + len(col_names['dynamic'])) * embed_dim)
    self.ad_embed_dim = (embed_dim * (1 + len(col_names['ad'])))
    expert = []
    for i in range(num_expert):
        expert.append(MultiLayerPerceptron(self.embed_output_dim, mlp_dims, dropout, False))
    self.mlp = nn.ModuleList(expert)
    output_layer = []
    for i in range(num_output):
        output_layer.append(Meta_Linear(mlp_dims[(- 1)], 1))
    self.output_layer = nn.ModuleList(output_layer)
    self.attention_layer = torch.nn.Sequential(Meta_Linear(self.ad_embed_dim, mlp_dims[(- 1)]), torch.nn.ReLU(), Meta_Linear(mlp_dims[(- 1)], num_expert), torch.nn.Softmax(dim=1))
    self.output_attention_layer = torch.nn.Sequential(Meta_Linear(self.ad_embed_dim, mlp_dims[(- 1)]), torch.nn.ReLU(), Meta_Linear(mlp_dims[(- 1)], num_output), torch.nn.Softmax(dim=1))
