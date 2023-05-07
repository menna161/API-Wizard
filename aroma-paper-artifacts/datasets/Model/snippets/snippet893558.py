import torch.nn as nn
from collections import OrderedDict
from torchmeta.modules import MetaModule, MetaConv2d, MetaBatchNorm2d, MetaSequential, MetaLinear


def ModelMLPSinusoid(hidden_sizes=[40, 40]):
    return MetaMLPModel(1, 1, hidden_sizes)
