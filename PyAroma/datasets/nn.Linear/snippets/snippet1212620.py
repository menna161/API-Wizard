import torch
import torch.nn as nn
import torch.nn.functional as F
from onmt.modules.sparse_activations import sparsemax
from onmt.utils.misc import aeq, sequence_mask


def __init__(self, dim, coverage=False, attn_type='dot', attn_func='softmax'):
    super(GlobalAttention, self).__init__()
    self.dim = dim
    assert (attn_type in ['dot', 'general', 'mlp']), 'Please select a valid attention type (got {:s}).'.format(attn_type)
    self.attn_type = attn_type
    assert (attn_func in ['softmax', 'sparsemax']), 'Please select a valid attention function.'
    self.attn_func = attn_func
    if (self.attn_type == 'general'):
        self.linear_in = nn.Linear(dim, dim, bias=False)
    elif (self.attn_type == 'mlp'):
        self.linear_context = nn.Linear(dim, dim, bias=False)
        self.linear_query = nn.Linear(dim, dim, bias=True)
        self.v = nn.Linear(dim, 1, bias=False)
    out_bias = (self.attn_type == 'mlp')
    self.linear_out = nn.Linear((dim * 2), dim, bias=out_bias)
    if coverage:
        self.linear_cover = nn.Linear(1, dim, bias=False)
