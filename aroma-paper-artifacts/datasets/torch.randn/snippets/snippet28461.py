import torch
import torch.nn as nn
from lib.sa.modules import Subtraction, Subtraction2, Aggregation

if (__name__ == '__main__'):
    net = san(sa_type=0, layers=(3, 4, 6, 8, 3), kernels=[3, 7, 7, 7, 7], num_classes=1000).cuda().eval()
    print(net)
    y = net(torch.randn(4, 3, 224, 224).cuda())
    print(y.size())
