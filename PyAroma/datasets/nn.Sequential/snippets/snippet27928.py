import torch
import torch.nn as nn
import torchvision


def __init__(self, cin, cout, nf=64, activation=nn.Tanh):
    super(Encoder, self).__init__()
    network = [nn.Conv2d(cin, nf, kernel_size=4, stride=2, padding=1, bias=False), nn.ReLU(inplace=True), nn.Conv2d(nf, (nf * 2), kernel_size=4, stride=2, padding=1, bias=False), nn.ReLU(inplace=True), nn.Conv2d((nf * 2), (nf * 4), kernel_size=4, stride=2, padding=1, bias=False), nn.ReLU(inplace=True), nn.Conv2d((nf * 4), (nf * 8), kernel_size=4, stride=2, padding=1, bias=False), nn.ReLU(inplace=True), nn.Conv2d((nf * 8), (nf * 8), kernel_size=4, stride=1, padding=0, bias=False), nn.ReLU(inplace=True), nn.Conv2d((nf * 8), cout, kernel_size=1, stride=1, padding=0, bias=False)]
    if (activation is not None):
        network += [activation()]
    self.network = nn.Sequential(*network)
