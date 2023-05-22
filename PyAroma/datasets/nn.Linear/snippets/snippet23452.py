import torch
import math
from torch import nn


def __init__(self, dim, heads=4, num_keys=128, topk=32, dim_head=256, input_dropout=0.0, query_dropout=0.0, value_dropout=0.0):
    super().__init__()
    assert ((dim % heads) == 0), 'dimension must be divisible by number of heads'
    self.topk = topk
    self.heads = heads
    self.num_keys = num_keys
    dim_query = (dim_head * heads)
    self.to_queries = nn.Linear(dim, dim_query, bias=False)
    self.norm = MaskedBatchNorm1D(nn.BatchNorm1d(dim_query))
    self.keys = nn.Parameter(torch.zeros(heads, num_keys, 2, (dim_head // 2)))
    self.values = nn.EmbeddingBag((num_keys ** 2), dim, mode='sum')
    init_(self.keys)
    init_(self.values.weight)
    self.input_dropout = nn.Dropout(input_dropout)
    self.query_dropout = nn.Dropout(query_dropout)
    self.value_dropout = nn.Dropout(value_dropout)
