import torch
from torchfm.layer import FeaturesEmbedding, CrossNetwork, MultiLayerPerceptron


def __init__(self, field_dims, embed_dim, num_layers, mlp_dims, dropout):
    super().__init__()
    self.embedding = FeaturesEmbedding(field_dims, embed_dim)
    self.embed_output_dim = (len(field_dims) * embed_dim)
    self.cn = CrossNetwork(self.embed_output_dim, num_layers)
    self.mlp = MultiLayerPerceptron(self.embed_output_dim, mlp_dims, dropout, output_layer=False)
    self.linear = torch.nn.Linear((mlp_dims[(- 1)] + self.embed_output_dim), 1)
