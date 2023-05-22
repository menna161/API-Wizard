import torch
import numpy as np
from .layer import FeaturesLinear, MultiLayerPerceptron, FeaturesEmbedding


def __init__(self, field_dims, embed_dim, sequence_length, lstm_dims, mlp_dims, dropouts):
    super().__init__()
    self.embedding = FeaturesEmbedding(field_dims, embed_dim)
    self.src_embedding = FeaturesEmbedding(field_dims, embed_dim)
    self.tgt_embedding = FeaturesEmbedding(field_dims, embed_dim)
    self.fc = torch.nn.Linear(in_features=(56 * embed_dim), out_features=embed_dim)
    self.src_fc = torch.nn.Linear(in_features=(56 * embed_dim), out_features=embed_dim)
    self.tgt_fc = torch.nn.Linear(in_features=(56 * embed_dim), out_features=embed_dim)
    self.bn = torch.nn.Sequential(torch.nn.BatchNorm1d(sequence_length), torch.nn.ReLU(), torch.nn.Dropout(dropouts[0]))
    self.src_bn = torch.nn.Sequential(torch.nn.BatchNorm1d(sequence_length), torch.nn.ReLU(), torch.nn.Dropout(dropouts[0]))
    self.tgt_bn = torch.nn.Sequential(torch.nn.BatchNorm1d(sequence_length), torch.nn.ReLU(), torch.nn.Dropout(dropouts[0]))
    self.linear = FeaturesLinear(field_dims)
    self.mlp = MultiLayerPerceptron((embed_dim + embed_dim), mlp_dims, dropouts[1])
    self.embed_dim = embed_dim
    self.src_domain_K = torch.nn.Linear(32, 32)
    self.src_domain_Q = torch.nn.Linear(32, 32)
    self.src_domain_V = torch.nn.Linear(32, 32)
    self.tgt_domain_K = torch.nn.Linear(32, 32)
    self.tgt_domain_Q = torch.nn.Linear(32, 32)
    self.tgt_domain_V = torch.nn.Linear(32, 32)
    self.lstm = torch.nn.LSTM(embed_dim, hidden_size=embed_dim, num_layers=1, batch_first=True, bidirectional=True)
    self.src_lstm = torch.nn.LSTM(embed_dim, hidden_size=embed_dim, num_layers=1, batch_first=True, bidirectional=True)
    self.tgt_lstm = torch.nn.LSTM(embed_dim, hidden_size=embed_dim, num_layers=1, batch_first=True, bidirectional=True)
