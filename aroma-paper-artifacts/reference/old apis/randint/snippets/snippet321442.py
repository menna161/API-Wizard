import torch
import numpy as np
from collections import OrderedDict
from torch import optim
from itertools import chain
from .swapgan import SwapGAN
from torch import nn
from torch.distributions import Dirichlet


def sampler(self, bs, f, is_2d, **kwargs):
    'Sampler function, which outputs an alpha which\n        you can use to produce a convex combination between\n        two examples.\n\n        :param bs: batch size\n        :param f: number of units / feature maps at encoding\n        :param is_2d: is the bottleneck a 2d tensor?\n        :returns: an alpha of shape `(bs, f)` is `is_2d` is set,\n          otherwise `(bs, f, 1, 1)`.\n        :rtype: \n\n        '
    if (self.mixer == 'mixup'):
        with torch.no_grad():
            alpha = self.dirichlet.sample_n(bs)
            if (not is_2d):
                alpha = alpha.reshape((- 1), alpha.size(1), 1, 1)
    elif (self.mixer == 'fm'):
        if is_2d:
            alpha = np.zeros((bs, self.k, f)).astype(np.float32)
        else:
            alpha = np.zeros((bs, self.k, f, 1, 1)).astype(np.float32)
        for b in range(bs):
            for j in range(f):
                alpha[(b, np.random.randint(0, self.k), j)] = 1.0
        alpha = torch.from_numpy(alpha).float()
    else:
        raise Exception(('Not implemented for mixup scheme: %s' % self.mixer))
    if self.use_cuda:
        alpha = alpha.cuda()
    return alpha
