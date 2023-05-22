import torch
import torch.nn as nn
import numpy as np
import copy


def __init__(self, in_channels=128, n_head=16, d_k=8, n_neurons=[256, 128], dropout=0.2, d_model=256, T=1000, len_max_seq=24, positions=None, return_att=False):
    '\n        Sequence-to-embedding encoder.\n        Args:\n            in_channels (int): Number of channels of the input embeddings\n            n_head (int): Number of attention heads\n            d_k (int): Dimension of the key and query vectors\n            n_neurons (list): Defines the dimensions of the successive feature spaces of the MLP that processes\n                the concatenated outputs of the attention heads\n            dropout (float): dropout\n            T (int): Period to use for the positional encoding\n            len_max_seq (int, optional): Maximum sequence length, used to pre-compute the positional encoding table\n            positions (list, optional): List of temporal positions to use instead of position in the sequence\n            d_model (int, optional): If specified, the input tensors will first processed by a fully connected layer\n                to project them into a feature space of dimension d_model\n            return_att (bool): If true, the module returns the attention masks along with the embeddings (default False)\n\n        '
    super(LTAE, self).__init__()
    self.in_channels = in_channels
    self.positions = positions
    self.n_neurons = copy.deepcopy(n_neurons)
    self.return_att = return_att
    if (positions is None):
        positions = (len_max_seq + 1)
    if (d_model is not None):
        self.d_model = d_model
        self.inconv = nn.Sequential(nn.Conv1d(in_channels, d_model, 1), nn.LayerNorm((d_model, len_max_seq)))
    else:
        self.d_model = in_channels
        self.inconv = None
    sin_tab = get_sinusoid_encoding_table(positions, (self.d_model // n_head), T=T)
    self.position_enc = nn.Embedding.from_pretrained(torch.cat([sin_tab for _ in range(n_head)], dim=1), freeze=True)
    self.inlayernorm = nn.LayerNorm(self.in_channels)
    self.outlayernorm = nn.LayerNorm(n_neurons[(- 1)])
    self.attention_heads = MultiHeadAttention(n_head=n_head, d_k=d_k, d_in=self.d_model)
    assert (self.n_neurons[0] == self.d_model)
    activation = nn.ReLU()
    layers = []
    for i in range((len(self.n_neurons) - 1)):
        layers.extend([nn.Linear(self.n_neurons[i], self.n_neurons[(i + 1)]), nn.BatchNorm1d(self.n_neurons[(i + 1)]), activation])
    self.mlp = nn.Sequential(*layers)
    self.dropout = nn.Dropout(dropout)
