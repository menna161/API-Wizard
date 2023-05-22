import torch
import torch.nn as nn
from torch.autograd import Variable
from torch._utils import _flatten_dense_tensors, _unflatten_dense_tensors


def network_to_half(network):
    '\n    Convert model to half precision in a batchnorm-safe way.\n\n    Retained for legacy purposes. It is recommended to use FP16Model.\n    '
    return nn.Sequential(tofp16(), BN_convert_float(network.half()))
