import torch
import numpy as np
from .layer import FeaturesLinear, MultiLayerPerceptron, FeaturesEmbedding


def __init__(self, field_dims, embed_dim, mlp_dims, dropout):
    super().__init__()
    self.embedding = FeaturesEmbedding(field_dims, embed_dim)
    self.src_embedding = FeaturesEmbedding(field_dims, embed_dim)
    self.tgt_embedding = FeaturesEmbedding(field_dims, embed_dim)
    self.embed_output_dim = ((11 * 56) * embed_dim)
    self.layer = torch.nn.Linear(self.embed_output_dim, 32)
    self.src_layer = torch.nn.Linear(self.embed_output_dim, 32)
    self.tgt_layer = torch.nn.Linear(self.embed_output_dim, 32)
    self.linear = FeaturesLinear(field_dims)
    self.mlp = MultiLayerPerceptron(32, mlp_dims, dropout)
    self.src_domain_K = torch.nn.Linear(32, 32)
    self.src_domain_Q = torch.nn.Linear(32, 32)
    self.src_domain_V = torch.nn.Linear(32, 32)
    self.tgt_domain_K = torch.nn.Linear(32, 32)
    self.tgt_domain_Q = torch.nn.Linear(32, 32)
    self.tgt_domain_V = torch.nn.Linear(32, 32)
