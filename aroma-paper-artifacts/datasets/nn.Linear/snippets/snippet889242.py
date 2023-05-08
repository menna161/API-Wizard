import torch
from .layer import FeaturesLinear, MultiLayerPerceptron, FeaturesEmbedding, FactorizationMachine


def __init__(self, field_dims, embed_dim, mlp_dims, dropouts):
    super().__init__()
    self.embedding = FeaturesEmbedding(field_dims, embed_dim)
    self.src_embedding = FeaturesEmbedding(field_dims, embed_dim)
    self.tgt_embedding = FeaturesEmbedding(field_dims, embed_dim)
    self.linear = FeaturesLinear(field_dims)
    self.fm = FactorizationMachine(reduce_sum=False)
    self.bn = torch.nn.Sequential(torch.nn.BatchNorm1d(embed_dim), torch.nn.Dropout(dropouts[0]))
    self.tgt_bn = torch.nn.Sequential(torch.nn.BatchNorm1d(embed_dim), torch.nn.Dropout(dropouts[0]))
    self.src_bn = torch.nn.Sequential(torch.nn.BatchNorm1d(embed_dim), torch.nn.Dropout(dropouts[0]))
    self.mlp = MultiLayerPerceptron(embed_dim, mlp_dims, dropouts[1])
    self.embed_dim = embed_dim
    self.src_domain_K = torch.nn.Linear(16, 16)
    self.src_domain_Q = torch.nn.Linear(16, 16)
    self.src_domain_V = torch.nn.Linear(16, 16)
    self.tgt_domain_K = torch.nn.Linear(16, 16)
    self.tgt_domain_Q = torch.nn.Linear(16, 16)
    self.tgt_domain_V = torch.nn.Linear(16, 16)
