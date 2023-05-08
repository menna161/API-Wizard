import torch
import torch.nn as nn
from torch.nn import functional as F
import math
from utils.tensor import chunk_two, cat_two, sum_except_batch as sumeb
from flows.transform import Transform

if (__name__ == '__main__'):

    class MLP(nn.Module):

        def __init__(self, dim_inputs, dim_outputs, dim_context=None):
            super().__init__()
            self.net = nn.Sequential(nn.Linear(dim_inputs, dim_outputs), nn.ELU(), nn.Linear(dim_outputs, dim_outputs))
            if (dim_context > 0):
                self.params_net = nn.Linear(dim_context, dim_outputs, bias=False)

        def forward(self, x, params=None):
            x = self.net(x)
            if ((params is not None) and (self.params_net is not None)):
                x += self.params_net(params)
            return x
    dim_inputs = 5
    dim_context = 10
    net_fn = (lambda d_in, d_out, d_con: MLP(d_in, d_out, d_con))
    layer = AffineCoupling(dim_inputs, net_fn, dim_context)
    x = torch.rand(10, dim_inputs)
    context = torch.rand(10, dim_context)
    (y, _) = layer(x, context)
    (xr, _) = layer.inverse(y, context)
    print((x - xr).mean())
    print(x[0])
    print(xr[0])
