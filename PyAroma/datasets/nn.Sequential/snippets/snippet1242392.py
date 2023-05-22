import torch
from torchfm.layer import FactorizationMachine, FeaturesEmbedding, MultiLayerPerceptron, FeaturesLinear


def __init__(self, field_dims, embed_dim, mlp_dims, dropouts):
    super().__init__()
    self.embedding = FeaturesEmbedding(field_dims, embed_dim)
    self.linear = FeaturesLinear(field_dims)
    self.fm = torch.nn.Sequential(FactorizationMachine(reduce_sum=False), torch.nn.BatchNorm1d(embed_dim), torch.nn.Dropout(dropouts[0]))
    self.mlp = MultiLayerPerceptron(embed_dim, mlp_dims, dropouts[1])
