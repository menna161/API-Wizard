import torch
from torchfm.layer import FeaturesEmbedding, MultiLayerPerceptron


def __init__(self, field_dims, user_field_idx, item_field_idx, embed_dim, mlp_dims, dropout):
    super().__init__()
    self.user_field_idx = user_field_idx
    self.item_field_idx = item_field_idx
    self.embedding = FeaturesEmbedding(field_dims, embed_dim)
    self.embed_output_dim = (len(field_dims) * embed_dim)
    self.mlp = MultiLayerPerceptron(self.embed_output_dim, mlp_dims, dropout, output_layer=False)
    self.fc = torch.nn.Linear((mlp_dims[(- 1)] + embed_dim), 1)
