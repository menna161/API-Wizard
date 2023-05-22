import torch
from torch.autograd import gradcheck
from gcn.layers.GConv import GOF_Function


def gradchecking(use_cuda=False):
    print(('-' * 80))
    GOF = GOF_Function.apply
    device = torch.device(('cuda' if use_cuda else 'cpu'))
    weight = torch.randn(8, 8, 4, 3, 3).to(device).double().requires_grad_()
    gfb = torch.randn(4, 3, 3).to(device).double()
    test = gradcheck(GOF, (weight, gfb), eps=1e-06, atol=0.0001, rtol=0.001, raise_exception=True)
    print(test)
