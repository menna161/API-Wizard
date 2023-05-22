import torch
import math


def __init__(self, scale, n_feat, bn=False, act='prelu', bias=True):
    super(Upsampler, self).__init__()
    modules = []
    for _ in range(int(math.log(scale, 2))):
        modules.append(ConvBlock(n_feat, (4 * n_feat), 3, 1, 1, bias, activation=None, norm=None))
        modules.append(torch.nn.PixelShuffle(2))
        if bn:
            modules.append(torch.nn.BatchNorm2d(n_feat))
    self.up = torch.nn.Sequential(*modules)
    self.activation = act
    if (self.activation == 'relu'):
        self.act = torch.nn.ReLU(True)
    elif (self.activation == 'prelu'):
        self.act = torch.nn.PReLU()
    elif (self.activation == 'lrelu'):
        self.act = torch.nn.LeakyReLU(0.2, True)
    elif (self.activation == 'tanh'):
        self.act = torch.nn.Tanh()
    elif (self.activation == 'sigmoid'):
        self.act = torch.nn.Sigmoid()
