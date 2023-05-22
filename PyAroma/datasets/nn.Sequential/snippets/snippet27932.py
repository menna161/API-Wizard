import torch
import torch.nn as nn
import torchvision


def __init__(self, cin, cout, zdim=128, nf=64):
    super(ConfNet, self).__init__()
    network = [nn.Conv2d(cin, nf, kernel_size=4, stride=2, padding=1, bias=False), nn.GroupNorm(16, nf), nn.LeakyReLU(0.2, inplace=True), nn.Conv2d(nf, (nf * 2), kernel_size=4, stride=2, padding=1, bias=False), nn.GroupNorm((16 * 2), (nf * 2)), nn.LeakyReLU(0.2, inplace=True), nn.Conv2d((nf * 2), (nf * 4), kernel_size=4, stride=2, padding=1, bias=False), nn.GroupNorm((16 * 4), (nf * 4)), nn.LeakyReLU(0.2, inplace=True), nn.Conv2d((nf * 4), (nf * 8), kernel_size=4, stride=2, padding=1, bias=False), nn.LeakyReLU(0.2, inplace=True), nn.Conv2d((nf * 8), zdim, kernel_size=4, stride=1, padding=0, bias=False), nn.ReLU(inplace=True)]
    network += [nn.ConvTranspose2d(zdim, (nf * 8), kernel_size=4, padding=0, bias=False), nn.ReLU(inplace=True), nn.ConvTranspose2d((nf * 8), (nf * 4), kernel_size=4, stride=2, padding=1, bias=False), nn.GroupNorm((16 * 4), (nf * 4)), nn.ReLU(inplace=True), nn.ConvTranspose2d((nf * 4), (nf * 2), kernel_size=4, stride=2, padding=1, bias=False), nn.GroupNorm((16 * 2), (nf * 2)), nn.ReLU(inplace=True)]
    self.network = nn.Sequential(*network)
    out_net1 = [nn.ConvTranspose2d((nf * 2), nf, kernel_size=4, stride=2, padding=1, bias=False), nn.GroupNorm(16, nf), nn.ReLU(inplace=True), nn.ConvTranspose2d(nf, nf, kernel_size=4, stride=2, padding=1, bias=False), nn.GroupNorm(16, nf), nn.ReLU(inplace=True), nn.Conv2d(nf, 2, kernel_size=5, stride=1, padding=2, bias=False), nn.Softplus()]
    self.out_net1 = nn.Sequential(*out_net1)
    out_net2 = [nn.Conv2d((nf * 2), 2, kernel_size=3, stride=1, padding=1, bias=False), nn.Softplus()]
    self.out_net2 = nn.Sequential(*out_net2)
