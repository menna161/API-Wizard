import torch
import torch.nn as nn
import torch.nn.functional as F
from flows.transform import Transform


def __init__(self, dim_inputs):
    super().__init__()
    self.dim_inputs = dim_inputs
    w_shape = [dim_inputs, dim_inputs]
    w_init = torch.qr(torch.randn(w_shape))[0]
    (p, lower, upper) = torch.lu_unpack(*torch.lu(w_init))
    s = torch.diag(upper)
    sign_s = torch.sign(s)
    log_s = torch.log(torch.abs(s))
    upper = torch.triu(upper, 1)
    l_mask = torch.tril(torch.ones(w_shape), (- 1))
    eye = torch.eye(*w_shape)
    self.register_buffer('p', p)
    self.register_buffer('sign_s', sign_s)
    self.lower = nn.Parameter(lower)
    self.log_s = nn.Parameter(log_s)
    self.upper = nn.Parameter(upper)
    self.register_buffer('l_mask', l_mask)
    self.register_buffer('eye', eye)
