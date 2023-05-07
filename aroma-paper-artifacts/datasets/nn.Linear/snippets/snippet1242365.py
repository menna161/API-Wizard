import torch
import torch.nn.functional as F
from torchfm.layer import FeaturesEmbedding, FeaturesLinear, MultiLayerPerceptron


def __init__(self, field_dims, embed_dim, atten_embed_dim, num_heads, num_layers, mlp_dims, dropouts, has_residual=True):
    super().__init__()
    self.num_fields = len(field_dims)
    self.linear = FeaturesLinear(field_dims)
    self.embedding = FeaturesEmbedding(field_dims, embed_dim)
    self.atten_embedding = torch.nn.Linear(embed_dim, atten_embed_dim)
    self.embed_output_dim = (len(field_dims) * embed_dim)
    self.atten_output_dim = (len(field_dims) * atten_embed_dim)
    self.has_residual = has_residual
    self.mlp = MultiLayerPerceptron(self.embed_output_dim, mlp_dims, dropouts[1])
    self.self_attns = torch.nn.ModuleList([torch.nn.MultiheadAttention(atten_embed_dim, num_heads, dropout=dropouts[0]) for _ in range(num_layers)])
    self.attn_fc = torch.nn.Linear(self.atten_output_dim, 1)
    if self.has_residual:
        self.V_res_embedding = torch.nn.Linear(embed_dim, atten_embed_dim)
