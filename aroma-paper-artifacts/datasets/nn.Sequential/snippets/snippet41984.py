import torch
import torch.nn as nn


def __init__(self, opt):
    super(Generator, self).__init__()
    self.is_cuda = torch.cuda.is_available()
    N = opt.nfc
    self.head = ConvBlock(opt.nc_im, N, ker_size=3, padd=1, stride=1)
    self.body = nn.Sequential()
    for i in range((opt.num_layer - 2)):
        N = int((opt.nfc / pow(2, (i + 1))))
        block = ConvBlock(max((2 * N), opt.min_nfc), max(N, opt.min_nfc), ker_size=3, padd=1, stride=1)
        self.body.add_module(('block%d' % (i + 1)), block)
    self.tail = nn.Sequential(nn.Conv2d(max(N, opt.min_nfc), opt.nc_im, kernel_size=3, stride=1, padding=1), nn.Tanh())
