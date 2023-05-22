import os.path as osp
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import torch.nn as nn


def get_parameters(self, bias=False):
    import torch.nn as nn
    modules_skipped = (nn.ReLU, nn.MaxPool2d, nn.Dropout2d, nn.Sequential, FCN8s)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            if bias:
                (yield m.bias)
            else:
                (yield m.weight)
        elif isinstance(m, nn.ConvTranspose2d):
            if bias:
                assert (m.bias is None)
        elif isinstance(m, modules_skipped):
            continue
        else:
            raise ValueError(('Unexpected module: %s' % str(m)))
