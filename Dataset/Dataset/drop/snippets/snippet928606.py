import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


def drop(self, delta):
    weight = (self.conv.weight * self.mask)
    print(weight.size())
    assert (weight.size()[(- 1)] == 1)
    weight = weight.abs().squeeze()
    assert (weight.size()[0] == self.out_channels)
    assert (weight.size()[1] == self.in_channels)
    d_out = (self.out_channels // self.groups)
    print(d_out.size())
    weight = weight.view(d_out, self.groups, self.in_channels)
    print(weight.size())
    weight = weight.transpose(0, 1).contiguous()
    print(weight.size())
    weight = weight.view(self.out_channels, self.in_channels)
    print(weight.size())
    for i in range(self.groups):
        wi = weight[((i * d_out):((i + 1) * d_out), :)]
        di = wi.sum(0).sort()[1][self.count:(self.count + delta)]
        for d in di.data:
            self._mask[(i::self.groups, d, :, :)].fill_(0)
    self.count = (self.count + delta)
