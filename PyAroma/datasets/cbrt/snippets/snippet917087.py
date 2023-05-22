import torch


def cbrt(x):
    'Cube root. Equivalent to torch.pow(x, 1/3), but numerically stable.'
    return (torch.sign(x) * torch.exp((torch.log(torch.abs(x)) / 3.0)))
