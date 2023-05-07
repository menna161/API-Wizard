import math
import torch
import torch.nn as nn
from onmt.utils.misc import generate_relative_positions_matrix, relative_matmul


def __init__(self, head_count, model_dim, dropout=0.1, max_relative_positions=0):
    assert ((model_dim % head_count) == 0)
    self.dim_per_head = (model_dim // head_count)
    self.model_dim = model_dim
    super(MultiHeadedAttention, self).__init__()
    self.head_count = head_count
    self.linear_keys = nn.Linear(model_dim, (head_count * self.dim_per_head))
    self.linear_values = nn.Linear(model_dim, (head_count * self.dim_per_head))
    self.linear_query = nn.Linear(model_dim, (head_count * self.dim_per_head))
    self.softmax = nn.Softmax(dim=(- 1))
    self.dropout = nn.Dropout(dropout)
    self.final_linear = nn.Linear(model_dim, model_dim)
    self.max_relative_positions = max_relative_positions
    if (max_relative_positions > 0):
        vocab_size = ((max_relative_positions * 2) + 1)
        self.relative_positions_embeddings = nn.Embedding(vocab_size, self.dim_per_head)
