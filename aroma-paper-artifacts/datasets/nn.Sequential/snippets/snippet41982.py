import torch
import torch.nn as nn


def __init__(self, opt):
    super(GeneratorConcatSkip2CleanAdd, self).__init__()
    self.is_cuda = torch.cuda.is_available()
    N = opt.nfc
    self.head = ConvBlock(opt.nc_im, N, opt.ker_size, opt.padd_size, 1)
    self.body = nn.Sequential()
    for i in range((opt.num_layer - 2)):
        N = int((opt.nfc / pow(2, (i + 1))))
        block = ConvBlock(max((2 * N), opt.min_nfc), max(N, opt.min_nfc), opt.ker_size, opt.padd_size, 1)
        self.body.add_module(('block%d' % (i + 1)), block)
    self.tail = nn.Sequential(nn.Conv2d(max(N, opt.min_nfc), opt.nc_im, kernel_size=opt.ker_size, stride=1, padding=opt.padd_size), nn.Tanh())
