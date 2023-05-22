import torch
import torch.nn as nn


def __init__(self, ngpu):
    super(Generator, self).__init__()
    self.ngpu = ngpu
    self.main = nn.Sequential(nn.ConvTranspose2d(nz, (ngf * 8), 4, 1, 0, bias=False), nn.BatchNorm2d((ngf * 8)), nn.ReLU(True), nn.ConvTranspose2d((ngf * 8), (ngf * 4), 4, 2, 1, bias=False), nn.BatchNorm2d((ngf * 4)), nn.ReLU(True), nn.ConvTranspose2d((ngf * 4), (ngf * 2), 4, 2, 1, bias=False), nn.BatchNorm2d((ngf * 2)), nn.ReLU(True), nn.ConvTranspose2d((ngf * 2), ngf, 4, 2, 1, bias=False), nn.BatchNorm2d(ngf), nn.ReLU(True), nn.ConvTranspose2d(ngf, nc, 4, 2, 1, bias=False), nn.Tanh())
